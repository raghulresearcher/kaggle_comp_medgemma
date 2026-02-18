"""
MedAdhere Pro - Flask Application Entry Point
"""
import logging
import threading
import json
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
from backend.config import config
from backend.firebase_client import adherence_service, patient_service

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize agent system
try:
    from backend.agents.agent_init import orchestrator
    logger.info("Agent system loaded successfully")
except Exception as e:
    logger.error(f"Failed to load agent system: {str(e)}")
    orchestrator = None

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config)

# Enable CORS for frontend communication
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize SocketIO for real-time communication
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# In-memory workflow storage (for demo - use Redis/Firebase in production)
workflow_results = {}


def serialize_workflow_result(result):
    """Convert workflow result to JSON-serializable format"""
    try:
        # Try direct JSON serialization first
        json.dumps(result)
        return result
    except (TypeError, ValueError):
        # Handle non-serializable objects
        if isinstance(result, dict):
            return {k: serialize_workflow_result(v) for k, v in result.items()}
        elif isinstance(result, list):
            return [serialize_workflow_result(item) for item in result]
        elif isinstance(result, datetime):
            return result.isoformat()
        elif hasattr(result, '__dict__'):
            # Handle Firebase Sentinel and other objects with attributes
            try:
                return {k: serialize_workflow_result(v) for k, v in result.__dict__.items()}
            except:
                return str(result)
        else:
            # Last resort: convert to string
            return str(result)


# ============================================================================
# Health Check Endpoints
# ============================================================================

@app.route("/")
def index():
    """Root endpoint - system status"""
    return jsonify({
        "service": "MedAdhere Pro - Agentic Backend",
        "version": "0.1.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "api_docs": "/api/docs",
            "patient_action": "/api/patient-action",
            "workflow_status": "/api/workflow-status/<workflow_id>",
            "workflows_list": "/api/workflows",
            "agent_query": "/api/agent-query",
            "stream_reasoning": "/api/stream-reasoning",
            "adherence_summary": "/api/adherence-summary"
        }
    })


@app.route("/api/health")
def health_check():
    """Health check endpoint"""
    agent_status = "initialized" if orchestrator and len(orchestrator.agents) == 5 else "not initialized"
    
    return jsonify({
        "status": "healthy",
        "medgemma_endpoint": config.MEDGEMMA_ENDPOINT,
        "medgemma_api_key_set": bool(config.MEDGEMMA_API_KEY),
        "firebase_configured": bool(config.FIREBASE_CREDENTIALS_PATH),
        "agents": {
            "status": agent_status,
            "count": len(orchestrator.agents) if orchestrator else 0
        }
    })


# ============================================================================
# API Endpoints (to be implemented)
# ============================================================================

@app.route("/api/patient-action", methods=["POST"])
def patient_action():
    """
    Log patient medication action and trigger agent workflow if needed
    
    Expected payload:
    {
        "patient_id": "p001",
        "action": "took|skipped|snoozed",
        "medication_id": "med_001",
        "reason": "timing_conflict|supplement_interference|side_effects|other",
        "timestamp": "2026-02-17T08:00:00Z",
        "notes": "optional user notes"
    }
    """
    try:
        data = request.json
        patient_id = data.get("patient_id")
        action = data.get("action")
        
        logger.info(f"Patient action received: {patient_id} - {action}")
        
        # Log action to Firebase
        log_id = adherence_service.log_action(data)
        logger.info(f"Action logged to Firebase: {log_id}")
        
        # Trigger agent workflow if appropriate
        if orchestrator and (action in ["skipped", "snoozed"] or (action == "took" and data.get("reason") == "side_effects")):
            logger.info(f"Triggering agent workflow for {action} action")
            
            # Run workflow asynchronously to avoid timeout
            workflow_id = f"wf_{patient_id}_{action}_{data.get('timestamp', '').replace(':', '').replace('-', '').replace('Z', '')[:14]}"
            
            def run_workflow():
                try:
                    logger.info(f"Starting async workflow: {workflow_id}")
                    workflow_result = orchestrator.route_patient_action(data)
                    logger.info(f"Workflow {workflow_id} completed: {workflow_result.get('state')}")
                    
                    # Store result for retrieval (serialize for JSON compatibility)
                    workflow_results[workflow_id] = {
                        "status": "completed",
                        "result": serialize_workflow_result(workflow_result),
                        "timestamp": data.get('timestamp'),
                        "completed_at": datetime.now().isoformat()
                    }
                except Exception as e:
                    logger.error(f"Workflow {workflow_id} error: {str(e)}")
                    workflow_results[workflow_id] = {
                        "status": "error",
                        "error": str(e),
                        "timestamp": data.get('timestamp'),
                        "failed_at": datetime.now().isoformat()
                    }
            
            # Mark workflow as started
            workflow_results[workflow_id] = {
                "status": "running",
                "started_at": data.get('timestamp') or datetime.now().isoformat()
            }
            
            thread = threading.Thread(target=run_workflow, daemon=True)
            thread.start()
            
            return jsonify({
                "status": "success",
                "message": "Action logged and workflow triggered (running asynchronously)",
                "workflow_id": workflow_id,
                "note": "Workflow is running in the background. Use SSE /api/stream-reasoning to monitor progress."
            })
        else:
            return jsonify({
                "status": "success",
                "message": "Action logged successfully",
                "agent_triggered": False
            })
        
    except Exception as e:
        logger.error(f"Error processing patient action: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/workflow-status/<workflow_id>", methods=["GET"])
def get_workflow_status(workflow_id):
    """
    Get status and results of a workflow execution
    
    Returns:
    {
        "workflow_id": "wf_p001_skipped_20260218...",
        "status": "running|completed|error",
        "result": {...},  // Only when completed
        "error": "...",   // Only when error
        "started_at": "timestamp"
    }
    """
    try:
        if workflow_id not in workflow_results:
            return jsonify({
                "status": "not_found",
                "message": f"Workflow {workflow_id} not found"
            }), 404
        
        workflow = workflow_results[workflow_id]
        return jsonify({
            "workflow_id": workflow_id,
            **workflow
        })
        
    except Exception as e:
        logger.error(f"Error retrieving workflow status: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/workflows", methods=["GET"])
def list_workflows():
    """
    List all workflow executions
    """
    try:
        return jsonify({
            "status": "success",
            "count": len(workflow_results),
            "workflows": [
                {"workflow_id": wf_id, **wf_data}
                for wf_id, wf_data in workflow_results.items()
            ]
        })
    except Exception as e:
        logger.error(f"Error listing workflows: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/agent-query", methods=["POST"])
def agent_query():
    """
    Trigger agent workflow for a specific patient query or issue
    
    Expected JSON body:
    {
        "patient_id": "p001",
        "query_type": "missed_dose",
        "context": {...}
    }
    """
    try:
        data = request.json
        patient_id = data.get("patient_id")
        query_type = data.get("query_type")
        
        logger.info(f"Agent query received: {patient_id} - {query_type}")
        
        if orchestrator:
            # Execute full workflow for explicit queries
            workflow_result = orchestrator.execute_workflow(data)
            
            return jsonify({
                "status": "success",
                "message": "Query processed by agent workflow",
                "workflow_id": workflow_result.get("workflow_id"),
                "agents_executed": len(workflow_result.get("agents_executed", [])),
                "workflow_state": workflow_result.get("state"),
                "result": workflow_result
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Agent system not initialized"
            }), 500
        
    except Exception as e:
        logger.error(f"Error processing agent query: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/stream-reasoning", methods=["GET"])
def stream_reasoning():
    """
    Server-Sent Events endpoint for streaming agent reasoning in real-time
    
    Query params:
    - workflow_id: The workflow to stream
    """
    from flask import Response
    import json
    import time
    
    def generate():
        workflow_id = request.args.get("workflow_id")
        
        if not orchestrator:
            yield f"data: {{\"error\": \"Agent system not initialized\"}}\n\n"
            return
        
        # Get workflow from orchestrator (if exists)
        workflow_data = orchestrator.active_workflows.get(workflow_id, {})
        
        if workflow_data:
            # Stream existing workflow steps
            for step in workflow_data.get("steps", []):
                yield f"data: {json.dumps(step)}\n\n"
                time.sleep(0.1)
        else:
            yield f"data: {{\"status\": \"waiting\", \"message\": \"Workflow {workflow_id} not found or not started\"}}\n\n"
    
    return Response(generate(), mimetype="text/event-stream")


@app.route("/api/adherence-summary/<patient_id>", methods=["GET"])
def adherence_summary(patient_id):
    """
    Get adherence summary and statistics for a patient
    """
    try:
        logger.info(f"Adherence summary requested for: {patient_id}")
        
        # TODO: Implement Firebase query
        
        return jsonify({
            "status": "success",
            "patient_id": patient_id,
            "summary": {
                "adherence_rate": 0.0,
                "streak_days": 0,
                "total_doses": 0,
                "missed_doses": 0
            }
        })
        
    except Exception as e:
        logger.error(f"Error fetching adherence summary: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================================================================
# WebSocket Events
# ============================================================================

@socketio.on("connect")
def handle_connect():
    """Handle WebSocket connection"""
    logger.info("Client connected to WebSocket")


@socketio.on("disconnect")
def handle_disconnect():
    """Handle WebSocket disconnection"""
    logger.info("Client disconnected from WebSocket")


@socketio.on("agent_subscribe")
def handle_agent_subscribe(data):
    """Subscribe to agent reasoning updates"""
    workflow_id = data.get("workflow_id")
    logger.info(f"Client subscribed to workflow: {workflow_id}")
    # TODO: Implement subscription logic


# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"status": "error", "message": "Internal server error"}), 500


# ============================================================================
# Application Entry Point
# ============================================================================

if __name__ == "__main__":
    try:
        logger.info(f"Starting MedAdhere Pro Backend on {config.HOST}:8000")
        logger.info(f"MedGemma Endpoint: {config.MEDGEMMA_ENDPOINT}")
        logger.info(f"MedGemma API Key Set: {bool(config.MEDGEMMA_API_KEY)}")
        
        # Use Flask's built-in server with threading enabled
        app.run(
            host=config.HOST,
            port=8000,
            debug=False,
            threaded=True,
            use_reloader=False
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
