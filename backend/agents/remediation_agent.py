"""
Remediation Agent - Creates personalized solutions
"""
import logging
from typing import Any, Dict, List
from backend.agents.base_agent import BaseAgent, AgentType

logger = logging.getLogger(__name__)


class RemediationAgent(BaseAgent):
    """
    Creates personalized remediation solutions based on investigation findings
    
    Responsibilities:
    - Design intervention strategies
    - Create specific action plans
    - Propose schedule adjustments
    - Generate patient-friendly recommendations
    """
    
    def __init__(self):
        super().__init__(AgentType.REMEDIATION)
        self.reasoning_steps = []
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input contains investigation results"""
        if "investigation_output" not in input_data:
            raise ValueError("investigation_output is required")
        return True
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create personalized remediation plan
        
        Args:
            input_data: Contains investigation findings
            
        Returns:
            Remediation plan with specific actions
        """
        self.reasoning_steps = []
        
        investigation = input_data.get("investigation_output", {})
        patient_id = input_data.get("patient_id")
        
        logger.info(f"Creating remediation plan for patient {patient_id}")
        self.reasoning_steps.append(f"💡 Remediation Agent started for patient {patient_id}")
        self.reasoning_steps.append(f"📝 Reviewing investigation findings...")
        
        # Check if pattern was detected
        if not investigation.get("pattern_detected"):
            self.reasoning_steps.append("ℹ️ No specific pattern - creating general support plan")
            plan = self._general_remediation()
            plan["reasoning"] = self.reasoning_steps
            return plan
        
        # Get root cause
        root_cause = investigation.get("root_cause", "")
        adherence_rate = investigation.get("adherence_rate", 0)
        self.reasoning_steps.append(f"🎯 Target: {root_cause}")
        self.reasoning_steps.append(f"📊 Current adherence: {adherence_rate}%")
        
        # Create targeted remediation plan
        plan = self._create_targeted_plan(root_cause, investigation)
        plan["reasoning"] = self.reasoning_steps
        
        return plan
    
    def _general_remediation(self) -> Dict[str, Any]:
        """Create general remediation when no pattern is found"""
        return {
            "plan_type": "general",
            "interventions": [
                {
                    "type": "encouragement",
                    "action": "Send positive reinforcement message",
                    "message": "Great job staying on track! Keep up the good work."
                }
            ],
            "priority": "low"
        }
    
    def _create_targeted_plan(
        self,
        root_cause: str,
        investigation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create targeted remediation plan based on root cause"""
        
        plan = {
            "plan_type": "targeted",
            "root_cause": root_cause,
            "interventions": [],
            "expected_outcome": "",
            "priority": "high"
        }
        
        # Behavioral pattern interventions
        if "Behavioral pattern" in root_cause:
            day_pattern = investigation.get("day_pattern", {})
            problem_day = day_pattern.get("problem_day")
            
            self.reasoning_steps.append(f"📆 Solution: Adjust {problem_day} schedule to account for routine")
            self.reasoning_steps.append(f"⏰ Recommendation: Move reminder 30 minutes earlier")
            self.reasoning_steps.append(f"📌 Add contextual anchor (e.g., 'before leaving for work')")
            
            plan["interventions"] = [
                {
                    "type": "schedule_adjustment",
                    "action": "Adjust reminder time for specific day",
                    "details": {
                        "target_day": problem_day,
                        "adjustment": "30 minutes earlier",
                        "reason": "Account for different morning routine"
                    }
                },
                {
                    "type": "contextual_reminder",
                    "action": "Add context-specific reminder",
                    "details": {
                        "context": f"{problem_day} morning routine",
                        "suggestion": "Set reminder before typical activity"
                    }
                }
            ]
            
            plan["expected_outcome"] = f"Reduce missed doses on {problem_day} by 80%"
        
        # Timing issue interventions
        elif "Timing issue" in root_cause:
            time_pattern = investigation.get("time_pattern", {})
            problem_time = time_pattern.get("problem_time")
            
            self.reasoning_steps.append(f"⏰ Solution: Shift medication from {problem_time} to more consistent time")
            self.reasoning_steps.append(f"🍽️ Anchor to meal time for better routine")
            
            # Suggest alternative times
            alternative_times = {
                "morning": ("evening", "after dinner"),
                "afternoon": ("morning", "with breakfast"),
                "evening": ("morning", "with breakfast"),
                "night": ("morning", "with breakfast")
            }
            
            alt_time, alt_context = alternative_times.get(problem_time, ("different time", "convenient moment"))
            
            plan["interventions"] = [
                {
                    "type": "time_shift",
                    "action": f"Shift reminder from {problem_time} to {alt_time}",
                    "details": {
                        "current_time": problem_time,
                        "proposed_time": alt_time,
                        "context": alt_context
                    }
                },
                {
                    "type": "meal_anchor",
                    "action": "Anchor to meal time",
                    "details": {
                        "anchor_event": alt_context,
                        "reason": "Meal times provide consistent routine"
                    }
                }
            ]
            
            plan["expected_outcome"] = f"Improve {problem_time} adherence from current rate to 90%+"
        
        # Memory/reminder interventions
        elif "Memory/reminder" in root_cause:
            self.reasoning_steps.append("🔔 Solution: Multi-stage reminder system")
            self.reasoning_steps.append("📢 Initial + 2 follow-ups + escalation if needed")
            self.reasoning_steps.append("⏸️ Smart snooze: 10-min intervals, max 3 times")
            
            plan["interventions"] = [
                {
                    "type": "reminder_frequency",
                    "action": "Increase reminder frequency",
                    "details": {
                        "initial_reminder": "Original scheduled time",
                        "follow_up_1": "5 minutes after",
                        "follow_up_2": "15 minutes after",
                        "escalation": "Alert if not taken within 30 minutes"
                    }
                },
                {
                    "type": "smart_snooze",
                    "action": "Implement smart snooze feature",
                    "details": {
                        "snooze_interval": "10 minutes",
                        "max_snoozes": 3,
                        "escalation_message": "Friendly reminder: medication still pending"
                    }
                }
            ]
            
            plan["expected_outcome"] = "Reduce 'forgot' incidents by 70%"
        
        # Supply chain interventions
        elif "Supply chain" in root_cause:
            self.reasoning_steps.append("📦 Solution: Automated refill management")
            self.reasoning_steps.append("🚨 Alert at 7 days remaining, auto-order at 5 days")
            self.reasoning_steps.append("🏪 Connect to preferred pharmacy for seamless refills")
            
            plan["interventions"] = [
                {
                    "type": "auto_refill",
                    "action": "Set up automatic refill",
                    "details": {
                        "trigger": "7 days before medication runs out",
                        "pharmacy": "Patient's preferred pharmacy",
                        "notification": "Confirm when refill is ready"
                    }
                },
                {
                    "type": "inventory_tracking",
                    "action": "Track medication inventory",
                    "details": {
                        "method": "Count remaining doses",
                        "alerts": ["14 days remaining", "7 days remaining", "3 days remaining"],
                        "action_required": "Initiate refill at 7-day alert"
                    }
                }
            ]
            
            plan["expected_outcome"] = "Zero medication gaps in next 90 days"
        
        # Tolerability interventions
        elif "Tolerability" in root_cause:
            self.reasoning_steps.append("⚕️ Solution: Side effect management strategy")
            self.reasoning_steps.append("🍽️ Timing: Take with food to reduce GI symptoms")
            self.reasoning_steps.append("🧠 Consult MedGemma: Validate severity and get professional guidance")
            
            plan["interventions"] = [
                {
                    "type": "timing_optimization",
                    "action": "Optimize medication timing for tolerability",
                    "details": {
                        "suggestion": "Take with food",
                        "meal_recommendation": "During or after largest meal",
                        "reason": "May reduce gastrointestinal side effects"
                    }
                },
                {
                    "type": "medgemma_consult",
                    "action": "Request MedGemma side effect assessment",
                    "details": {
                        "priority": "high",
                        "questions": [
                            "Is this side effect common?",
                            "Will it diminish over time?",
                            "When should patient see doctor?"
                        ]
                    }
                }
            ]
            
            plan["expected_outcome"] = "Side effects managed or resolved within 7 days"
        
        # Default plan
        else:
            self.reasoning_steps.append("Creating monitoring plan for unclear pattern")
            
            plan["interventions"] = [
                {
                    "type": "enhanced_monitoring",
                    "action": "Increase monitoring frequency",
                    "details": {
                        "check_in_frequency": "Daily",
                        "data_to_collect": ["Mood", "Context when missed", "Time of day"],
                        "duration": "14 days"
                    }
                }
            ]
            
            plan["expected_outcome"] = "Clear pattern emerges within 2 weeks"
        
        self.reasoning_steps.append(f"✅ Created {len(plan['interventions'])}-part intervention plan")
        self.reasoning_steps.append(f"🎯 Expected outcome: {plan['expected_outcome']}")
        
        return plan
    
    def get_reasoning_steps(self) -> List[str]:
        """Return reasoning steps for transparency"""
        return self.reasoning_steps
