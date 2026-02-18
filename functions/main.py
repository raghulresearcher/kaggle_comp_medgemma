"""
MedAdhere Pro - Firebase Cloud Functions
"""
import json
import logging
from datetime import datetime
from firebase_functions import https_fn, options
from firebase_admin import initialize_app, firestore
import sys
import os

# Add backend to path to import existing modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.firebase_client import adherence_service, patient_service
from backend.agents.agent_init import orchestrator

# Initialize Firebase Admin
initialize_app()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory workflow storage (for demo)
workflow_results = {}


def serialize_workflow_result(result):
    """Convert workflow result to JSON-serializable format"""
    try:
        json.dumps(result)
        return result
    except (TypeError, ValueError):
        if isinstance(result, dict):
            return {k: serialize_workflow_result(v) for k, v in result.items()}
        elif isinstance(result, list):
            return [serialize_workflow_result(item) for item in result]
        elif isinstance(result, datetime):
            return result.isoformat()
        elif hasattr(result, '__dict__'):
            try:
                return {k: serialize_workflow_result(v) for k, v in result.__dict__.items()}
            except:
                return str(result)
        else:
            return str(result)


@https_fn.on_request(
    cors=options.CorsOptions(
        cors_origins="*",
        cors_methods=["GET", "POST", "OPTIONS"]
    ),
    memory=options.MemoryOption.GB_1,
    timeout_sec=540  # 9 minutes for MedGemma processing
)
def api_patient_action(req: https_fn.Request) -> https_fn.Response:
    """
    Log patient medication action and trigger agent workflow
    
    POST /api/patient-action
    Body: {
        "patient_id": "p001",
        "action": "took|skipped|snoozed",
        "medication_id": "med_001",
        "reason": "forgot|ran_out|side_effects|other",
        "timestamp": "2026-02-17T08:00:00Z",
        "notes": "optional user notes"
    }
    """
    if req.method == "OPTIONS":
        return https_fn.Response("", status=204)
    
    try:
        data = req.get_json()
        patient_id = data.get("patient_id")
        action = data.get("action")
        
        logger.info(f"Patient action received: {patient_id} - {action}")
        
        # Log action to Firebase
        log_id = adherence_service.log_action(data)
        logger.info(f"Action logged to Firebase: {log_id}")
        
        # Trigger agent workflow if appropriate
        if orchestrator and action in ["skipped", "snoozed"]:
            logger.info(f"Triggering agent workflow for {action} action")
            
            workflow_id = f"wf_{patient_id}_{action}_{data.get('timestamp', '').replace(':', '').replace('-', '').replace('Z', '')[:14]}"
            
            # Run workflow synchronously (Cloud Functions handle timeout)
            workflow_result = orchestrator.route_patient_action(data)
            
            # Store result
            workflow_results[workflow_id] = {
                "status": "completed",
                "result": serialize_workflow_result(workflow_result),
                "timestamp": data.get('timestamp'),
                "completed_at": datetime.now().isoformat()
            }
            
            return https_fn.Response(
                json.dumps({
                    "status": "success",
                    "message": "Action logged and workflow completed",
                    "workflow_id": workflow_id,
                    "result": serialize_workflow_result(workflow_result)
                }),
                status=200,
                mimetype="application/json"
            )
        else:
            return https_fn.Response(
                json.dumps({
                    "status": "success",
                    "message": "Action logged successfully",
                    "agent_triggered": False
                }),
                status=200,
                mimetype="application/json"
            )
        
    except Exception as e:
        logger.error(f"Error processing patient action: {str(e)}")
        return https_fn.Response(
            json.dumps({"status": "error", "message": str(e)}),
            status=500,
            mimetype="application/json"
        )


@https_fn.on_request(
    cors=options.CorsOptions(
        cors_origins="*",
        cors_methods=["GET", "OPTIONS"]
    )
)
def api_workflow_status(req: https_fn.Request) -> https_fn.Response:
    """
    Get status and results of a workflow execution
    
    GET /api/workflow-status/{workflow_id}
    """
    if req.method == "OPTIONS":
        return https_fn.Response("", status=204)
    
    try:
        # Extract workflow_id from path
        path_parts = req.path.split('/')
        workflow_id = path_parts[-1] if path_parts else None
        
        if not workflow_id:
            return https_fn.Response(
                json.dumps({"status": "error", "message": "workflow_id required"}),
                status=400,
                mimetype="application/json"
            )
        
        result = workflow_results.get(workflow_id)
        
        if result:
            return https_fn.Response(
                json.dumps({
                    "workflow_id": workflow_id,
                    **result
                }),
                status=200,
                mimetype="application/json"
            )
        else:
            return https_fn.Response(
                json.dumps({
                    "status": "not_found",
                    "message": f"Workflow {workflow_id} not found"
                }),
                status=404,
                mimetype="application/json"
            )
    
    except Exception as e:
        logger.error(f"Error retrieving workflow status: {str(e)}")
        return https_fn.Response(
            json.dumps({"status": "error", "message": str(e)}),
            status=500,
            mimetype="application/json"
        )


@https_fn.on_request(
    cors=options.CorsOptions(
        cors_origins="*",
        cors_methods=["GET", "OPTIONS"]
    )
)
def api_workflows(req: https_fn.Request) -> https_fn.Response:
    """
    Get list of all workflows
    
    GET /api/workflows
    """
    if req.method == "OPTIONS":
        return https_fn.Response("", status=204)
    
    try:
        workflows = [
            {
                "workflow_id": wf_id,
                "status": data["status"],
                "timestamp": data["timestamp"],
                "completed_at": data.get("completed_at")
            }
            for wf_id, data in workflow_results.items()
        ]
        
        return https_fn.Response(
            json.dumps({
                "status": "success",
                "count": len(workflows),
                "workflows": workflows
            }),
            status=200,
            mimetype="application/json"
        )
    
    except Exception as e:
        logger.error(f"Error listing workflows: {str(e)}")
        return https_fn.Response(
            json.dumps({"status": "error", "message": str(e)}),
            status=500,
            mimetype="application/json"
        )


@https_fn.on_request(
    cors=options.CorsOptions(
        cors_origins="*",
        cors_methods=["GET", "OPTIONS"]
    )
)
def api_health(req: https_fn.Request) -> https_fn.Response:
    """
    Health check endpoint
    
    GET /api/health
    """
    if req.method == "OPTIONS":
        return https_fn.Response("", status=204)
    
    try:
        agent_status = "initialized" if orchestrator and len(orchestrator.agents) > 0 else "not initialized"
        
        return https_fn.Response(
            json.dumps({
                "status": "healthy",
                "service": "MedAdhere Pro - Cloud Functions",
                "agents": {
                    "status": agent_status,
                    "count": len(orchestrator.agents) if orchestrator else 0
                },
                "firebase_configured": True
            }),
            status=200,
            mimetype="application/json"
        )
    
    except Exception as e:
        return https_fn.Response(
            json.dumps({"status": "error", "message": str(e)}),
            status=500,
            mimetype="application/json"
        )
