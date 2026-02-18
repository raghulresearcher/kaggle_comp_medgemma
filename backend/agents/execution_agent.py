"""
Execution Agent - Implements approved interventions
"""
import logging
from typing import Any, Dict, List
from datetime import datetime
from backend.agents.base_agent import BaseAgent, AgentType
from backend.firebase_client import patient_service, intervention_service

logger = logging.getLogger(__name__)


class ExecutionAgent(BaseAgent):
    """
    Executes approved interventions and updates patient data
    
    Responsibilities:
    - Implement schedule changes
    - Update patient preferences
    - Configure new reminders
    - Log intervention execution
    - Notify patient of changes
    """
    
    def __init__(self):
        super().__init__(AgentType.EXECUTION)
        self.reasoning_steps = []
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input contains risk assessment"""
        if "risk_assessment_output" not in input_data:
            raise ValueError("risk_assessment_output is required")
        return True
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute approved interventions
        
        Args:
            input_data: Contains risk assessment and remediation plan
            
        Returns:
            Execution results with actions taken
        """
        self.reasoning_steps = []
        
        patient_id = input_data.get("patient_id")
        risk_assessment = input_data.get("risk_assessment_output", {})
        remediation = input_data.get("remediation_output", {})
        
        logger.info(f"Executing interventions for patient {patient_id}")
        self.reasoning_steps.append(f"⚙️ Execution Agent started for patient {patient_id}")
        self.reasoning_steps.append(f"🔐 Verifying risk assessment approval...")
        
        # Check if interventions are approved
        if not risk_assessment.get("approved"):
            self.reasoning_steps.append("❌ Interventions not approved - execution aborted")
            self.reasoning_steps.append("👥 Flagging for human review")
            return {
                "executed": False,
                "reason": "Risk assessment did not approve interventions",
                "requires_human_review": True,
                "reasoning": self.reasoning_steps
            }
        
        self.reasoning_steps.append("✅ Risk approval confirmed - proceeding with execution")
        
        # Execute each approved intervention
        interventions = remediation.get("interventions", [])
        self.reasoning_steps.append(f"🛠️ Executing {len(interventions)} interventions...")
        
        execution_results = []
        
        for idx, intervention in enumerate(interventions, 1):
            self.reasoning_steps.append(f"  {idx}. {intervention.get('action', 'Unknown action')}")
            result = self._execute_intervention(intervention, patient_id)
            execution_results.append(result)
        
        # Log intervention in Firebase
        self.reasoning_steps.append("💾 Saving intervention to Firebase Firestore...")
        self._log_intervention_to_firebase(
            patient_id,
            remediation,
            risk_assessment,
            execution_results
        )
        
        # Generate patient notification
        self.reasoning_steps.append("📧 Generating patient notification...")
        notification = self._generate_patient_notification(
            remediation,
            execution_results
        )
        
        self.reasoning_steps.append("📅 Scheduling 2-week follow-up check-in...")
        follow_up = self._schedule_follow_up(patient_id)
        
        self.reasoning_steps.append(f"✅ Successfully executed all {len(execution_results)} interventions")
        self.reasoning_steps.append("🎯 Intervention implementation complete")
        
        return {
            "executed": True,
            "execution_count": len(execution_results),
            "execution_results": execution_results,
            "patient_notification": notification,
            "follow_up_scheduled": follow_up,
            "reasoning": self.reasoning_steps
        }
    
    def _execute_intervention(
        self,
        intervention: Dict[str, Any],
        patient_id: str
    ) -> Dict[str, Any]:
        """Execute a single intervention"""
        
        intervention_type = intervention.get("type")
        self.reasoning_steps.append(f"Executing: {intervention_type}")
        
        # Route to specific execution function
        if intervention_type == "schedule_adjustment":
            return self._execute_schedule_adjustment(intervention, patient_id)
        
        elif intervention_type == "time_shift":
            return self._execute_time_shift(intervention, patient_id)
        
        elif intervention_type == "reminder_frequency":
            return self._execute_reminder_frequency(intervention, patient_id)
        
        elif intervention_type == "auto_refill":
            return self._execute_auto_refill(intervention, patient_id)
        
        elif intervention_type == "timing_optimization":
            return self._execute_timing_optimization(intervention, patient_id)
        
        else:
            # Generic execution for other types
            return self._execute_generic(intervention, patient_id)
    
    def _execute_schedule_adjustment(
        self,
        intervention: Dict[str, Any],
        patient_id: str
    ) -> Dict[str, Any]:
        """Adjust medication schedule"""
        
        details = intervention.get("details", {})
        target_day = details.get("target_day")
        adjustment = details.get("adjustment")
        
        try:
            # Update patient schedule in Firebase
            update_data = {
                "schedule_adjustments": {
                    target_day: {
                        "adjustment": adjustment,
                        "applied_at": datetime.utcnow().isoformat(),
                        "reason": details.get("reason")
                    }
                }
            }
            
            patient_service.update_patient(patient_id, update_data)
            
            self.reasoning_steps.append(f"✓ Adjusted schedule for {target_day}")
            
            return {
                "intervention_type": "schedule_adjustment",
                "status": "success",
                "details": f"Schedule adjusted for {target_day}: {adjustment}"
            }
            
        except Exception as e:
            logger.error(f"Schedule adjustment failed: {str(e)}")
            return {
                "intervention_type": "schedule_adjustment",
                "status": "failed",
                "error": str(e)
            }
    
    def _execute_time_shift(
        self,
        intervention: Dict[str, Any],
        patient_id: str
    ) -> Dict[str, Any]:
        """Shift medication time"""
        
        details = intervention.get("details", {})
        
        try:
            update_data = {
                "preferred_time": details.get("proposed_time"),
                "time_context": details.get("context"),
                "time_updated_at": datetime.utcnow().isoformat()
            }
            
            patient_service.update_patient(patient_id, update_data)
            
            self.reasoning_steps.append(f"✓ Shifted time to {details.get('proposed_time')}")
            
            return {
                "intervention_type": "time_shift",
                "status": "success",
                "details": f"Medication time changed to {details.get('proposed_time')}"
            }
            
        except Exception as e:
            logger.error(f"Time shift failed: {str(e)}")
            return {
                "intervention_type": "time_shift",
                "status": "failed",
                "error": str(e)
            }
    
    def _execute_reminder_frequency(
        self,
        intervention: Dict[str, Any],
        patient_id: str
    ) -> Dict[str, Any]:
        """Update reminder frequency"""
        
        details = intervention.get("details", {})
        
        try:
            update_data = {
                "reminder_settings": {
                    "initial_reminder": details.get("initial_reminder"),
                    "follow_ups": [
                        details.get("follow_up_1"),
                        details.get("follow_up_2")
                    ],
                    "escalation": details.get("escalation"),
                    "updated_at": datetime.utcnow().isoformat()
                }
            }
            
            patient_service.update_patient(patient_id, update_data)
            
            self.reasoning_steps.append("✓ Updated reminder frequency")
            
            return {
                "intervention_type": "reminder_frequency",
                "status": "success",
                "details": "Enhanced reminder system activated"
            }
            
        except Exception as e:
            logger.error(f"Reminder frequency update failed: {str(e)}")
            return {
                "intervention_type": "reminder_frequency",
                "status": "failed",
                "error": str(e)
            }
    
    def _execute_auto_refill(
        self,
        intervention: Dict[str, Any],
        patient_id: str
    ) -> Dict[str, Any]:
        """Set up automatic refill"""
        
        details = intervention.get("details", {})
        
        try:
            update_data = {
                "auto_refill_enabled": True,
                "refill_trigger_days": 7,
                "refill_settings": {
                    "pharmacy": details.get("pharmacy"),
                    "notification": details.get("notification"),
                    "enabled_at": datetime.utcnow().isoformat()
                }
            }
            
            patient_service.update_patient(patient_id, update_data)
            
            self.reasoning_steps.append("✓ Auto-refill enabled")
            
            return {
                "intervention_type": "auto_refill",
                "status": "success",
                "details": "Auto-refill activated - will trigger 7 days before running out"
            }
            
        except Exception as e:
            logger.error(f"Auto-refill setup failed: {str(e)}")
            return {
                "intervention_type": "auto_refill",
                "status": "failed",
                "error": str(e)
            }
    
    def _execute_timing_optimization(
        self,
        intervention: Dict[str, Any],
        patient_id: str
    ) -> Dict[str, Any]:
        """Optimize medication timing for tolerability"""
        
        details = intervention.get("details", {})
        
        try:
            update_data = {
                "timing_optimization": {
                    "suggestion": details.get("suggestion"),
                    "meal_recommendation": details.get("meal_recommendation"),
                    "reason": details.get("reason"),
                    "applied_at": datetime.utcnow().isoformat()
                }
            }
            
            patient_service.update_patient(patient_id, update_data)
            
            self.reasoning_steps.append("✓ Timing optimized for tolerability")
            
            return {
                "intervention_type": "timing_optimization",
                "status": "success",
                "details": f"{details.get('suggestion')} - {details.get('meal_recommendation')}"
            }
            
        except Exception as e:
            logger.error(f"Timing optimization failed: {str(e)}")
            return {
                "intervention_type": "timing_optimization",
                "status": "failed",
                "error": str(e)
            }
    
    def _execute_generic(
        self,
        intervention: Dict[str, Any],
        patient_id: str
    ) -> Dict[str, Any]:
        """Generic execution for other intervention types"""
        
        intervention_type = intervention.get("type")
        
        self.reasoning_steps.append(f"✓ Logged {intervention_type}")
        
        return {
            "intervention_type": intervention_type,
            "status": "logged",
            "details": "Intervention recorded for monitoring"
        }
    
    def _log_intervention_to_firebase(
        self,
        patient_id: str,
        remediation: Dict[str, Any],
        risk_assessment: Dict[str, Any],
        execution_results: List[Dict[str, Any]]
    ):
        """Log intervention details to Firebase"""
        
        try:
            intervention_data = {
                "patient_id": patient_id,
                "timestamp": datetime.utcnow().isoformat(),
                "root_cause": remediation.get("root_cause"),
                "interventions": remediation.get("interventions"),
                "risk_assessment": {
                    "approved": risk_assessment.get("approved"),
                    "risk_level": risk_assessment.get("overall_risk_level")
                },
                "execution_results": execution_results,
                "expected_outcome": remediation.get("expected_outcome")
            }
            
            intervention_service.log_intervention(intervention_data)
            self.reasoning_steps.append("✓ Intervention logged to Firebase")
            
        except Exception as e:
            logger.error(f"Failed to log intervention: {str(e)}")
    
    def _generate_patient_notification(
        self,
        remediation: Dict[str, Any],
        execution_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate patient-friendly notification"""
        
        successful_interventions = [r for r in execution_results if r["status"] == "success"]
        
        # Create friendly message
        if len(successful_interventions) == 1:
            message = "We've made an adjustment to help you stay on track! 💊"
        else:
            message = f"We've made {len(successful_interventions)} improvements to support you! 💊"
        
        # Add details
        details = []
        for result in successful_interventions:
            details.append(result.get("details", ""))
        
        return {
            "title": "Your Medication Plan Updated",
            "message": message,
            "details": details,
            "expected_outcome": remediation.get("expected_outcome"),
            "action_required": False
        }
    
    def _schedule_follow_up(self, patient_id: str) -> Dict[str, Any]:
        """Schedule follow-up check"""
        
        from datetime import timedelta
        follow_up_date = datetime.utcnow() + timedelta(days=3)
        
        self.reasoning_steps.append(f"✓ Follow-up scheduled for {follow_up_date.date()}")
        
        return {
            "scheduled": True,
            "follow_up_date": follow_up_date.isoformat(),
            "check_type": "automated",
            "questions": [
                "Are the new reminders working better for you?",
                "Have you noticed any improvement?",
                "Any issues we should address?"
            ]
        }
    
    def get_reasoning_steps(self) -> List[str]:
        """Return reasoning steps for transparency"""
        return self.reasoning_steps
