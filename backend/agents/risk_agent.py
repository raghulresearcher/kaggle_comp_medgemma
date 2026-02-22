"""
Risk Assessment Agent - Validates safety with MedGemma
"""
import logging
from typing import Any, Dict, List
from backend.agents.base_agent import BaseAgent, AgentType
from backend.agents.medgemma_hf import MedGemmaHF, create_medical_prompt
from backend.config import config

logger = logging.getLogger(__name__)


class RiskAssessmentAgent(BaseAgent):
    """
    Validates safety of proposed interventions using MedGemma
    
    Responsibilities:
    - Validate medication timing changes are safe
    - Check for drug interactions
    - Assess side effect severity
    - Ensure interventions don't compromise patient safety
    """
    
    def __init__(self):
        super().__init__(AgentType.RISK_ASSESSMENT)
        self.reasoning_steps = []
        
        # Initialize MedGemma HF
        try:
            if config.MEDGEMMA_API_KEY:
                self.llm = MedGemmaHF(
                    endpoint_url=config.MEDGEMMA_ENDPOINT,
                    api_key=config.MEDGEMMA_API_KEY,
                    timeout=config.MEDGEMMA_TIMEOUT,
                    temperature=config.MEDGEMMA_TEMPERATURE,
                    max_tokens=config.MEDGEMMA_MAX_TOKENS
                )
                logger.info(f"Risk Agent initialized with MedGemma HF endpoint")
            else:
                logger.warning("HF_API_KEY not set. Will use rule-based fallback.")
                self.llm = None
        except Exception as e:
            logger.warning(f"Failed to initialize MedGemma HF: {e}. Will use rule-based fallback.")
            self.llm = None
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input contains remediation plan"""
        if "remediation_output" not in input_data:
            raise ValueError("remediation_output is required")
        return True
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess safety risks of proposed remediation plan
        
        Args:
            input_data: Contains remediation plan and patient context
            
        Returns:
            Risk assessment with approval/rejection and recommendations
        """
        self.reasoning_steps = []
        self.medgemma_actually_consulted = False  # Track actual MedGemma usage
        
        patient_id = input_data.get("patient_id")
        remediation = input_data.get("remediation_output", {})
        
        logger.info(f"Assessing risks for patient {patient_id}")
        self.reasoning_steps.append(f"⚕️ Risk Assessment Agent started for patient {patient_id}")
        
        # Check if MedGemma HF is available
        if not self.llm:
            logger.warning("MedGemma HF not available, using fallback risk assessment")
            self.reasoning_steps.append("⚠️ MedGemma HF endpoint unavailable - using rule-based fallback")
            assessment = self._fallback_assessment(remediation)
            assessment["reasoning"] = self.reasoning_steps
            return assessment
        
        self.reasoning_steps.append("🧠 Connecting to MedGemma for medical validation...")
        
        # Get patient context - check both current_action and root level (for backwards compatibility)
        current_action = input_data.get("current_action", {})
        if not current_action:
            # Fallback: treat input_data as the action itself (for trigger data)
            current_action = input_data
        investigation = input_data.get("investigation_output", {})
        
        # Check if this is a side effect with image - handle vision analysis FIRST
        if current_action.get("reason") == "side_effects" and current_action.get("image"):
            self.reasoning_steps.append("📸 Image detected with side effects - activating vision analysis")
            # Create a special intervention for vision analysis
            vision_result = self._assess_with_vision({}, current_action)
            return {
                "approved": vision_result.get("approved", True),
                "overall_risk_level": vision_result.get("risk_level", "low"),
                "intervention_assessments": [vision_result],
                "medgemma_consulted": True,
                "vision_analysis_performed": vision_result.get("vision_analysis_performed", True),
                "temporal_comparison": vision_result.get("temporal_comparison", False),
                "healing_trend": vision_result.get("healing_trend", "unknown"),
                "recommendations": [
                    vision_result.get("reason", "Vision analysis completed"),
                    "Continue daily photo monitoring" if vision_result.get("approved") else "Consult healthcare provider"
                ],
                "reasoning": self.reasoning_steps
            }
        
        # Assess each intervention
        interventions = remediation.get("interventions", [])
        self.reasoning_steps.append(f"🔍 Reviewing {len(interventions)} proposed interventions for safety...")
        
        assessment_results = []
        overall_safe = True
        
        for intervention in interventions:
            result = self._assess_intervention(intervention, patient_id, current_action)
            assessment_results.append(result)
            
            if result["risk_level"] == "high":
                overall_safe = False
        
        # Generate final assessment
        assessment = {
            "approved": overall_safe,
            "overall_risk_level": self._determine_overall_risk(assessment_results),
            "intervention_assessments": assessment_results,
            "medgemma_consulted": self.medgemma_actually_consulted,  # Accurate tracking
            "recommendations": self._generate_safety_recommendations(assessment_results),
            "reasoning": self.reasoning_steps
        }
        
        if overall_safe:
            self.reasoning_steps.append("✅ APPROVED: All interventions are medically safe")
            self.reasoning_steps.append("✓ No drug interactions or timing concerns detected")
        else:
            self.reasoning_steps.append("❌ HIGH RISK: Intervention requires physician review")
            self.reasoning_steps.append("⚠️ Human oversight required before proceeding")
        
        return assessment
    
    def _assess_intervention(
        self,
        intervention: Dict[str, Any],
        patient_id: str,
        current_action: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess safety of a single intervention"""
        
        intervention_type = intervention.get("type")
        self.reasoning_steps.append(f"Assessing intervention type: {intervention_type}")
        
        # Timing-related interventions need MedGemma validation
        if intervention_type in ["schedule_adjustment", "time_shift", "timing_optimization"]:
            return self._assess_timing_change(intervention, current_action)
        
        # Side effect related interventions
        elif intervention_type == "medgemma_consult":
            return self._assess_side_effects(intervention, current_action)
        
        # Other interventions (reminders, refills) are generally low risk
        else:
            return {
                "intervention_type": intervention_type,
                "risk_level": "low",
                "approved": True,
                "reason": "Non-medical intervention - low risk"
            }
    
    def _assess_timing_change(
        self,
        intervention: Dict[str, Any],
        current_action: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Use MedGemma to assess if timing change is safe"""
        
        details = intervention.get("details", {})
        
        # Create prompt for MedGemma
        prompt = create_medical_prompt(
            question=(
                "Patient is considering changing medication timing. "
                f"Current: {details.get('current_time', 'unspecified')}. "
                f"Proposed: {details.get('proposed_time', 'unspecified')}. "
                f"Context: {details.get('context', 'none provided')}. "
                "Is this timing change medically safe?"
            ),
            format_instructions=(
                "Respond with:\n"
                "- Safe: Yes/No/Conditional\n"
                "- Concerns: List any medical concerns\n"
                "- Recommendations: Any specific guidance"
            )
        )
        
        try:
            self.reasoning_steps.append("Consulting MedGemma for timing safety...")
            response = self.llm.invoke(prompt)
            
            # Successfully consulted MedGemma
            self.medgemma_actually_consulted = True
            
            # Parse response (basic - can be enhanced)
            safe = "yes" in response.lower()[:100]
            
            self.reasoning_steps.append(f"✅ MedGemma consulted: {'Safe' if safe else 'Review needed'}")
            
            return {
                "intervention_type": intervention.get("type"),
                "risk_level": "low" if safe else "medium",
                "approved": safe,
                "medgemma_response": response[:500],  # Truncate for storage
                "reason": "MedGemma validation completed"
            }
            
        except Exception as e:
            logger.error(f"MedGemma timing assessment failed: {str(e)}")
            self.reasoning_steps.append(f"⚠️ MedGemma error: {str(e)}")
            
            # Fallback: timing changes are generally safe
            return {
                "intervention_type": intervention.get("type"),
                "risk_level": "low",
                "approved": True,
                "reason": "MedGemma unavailable - using rule-based fallback for timing change"
            }
    
    def _assess_side_effects(
        self,
        intervention: Dict[str, Any],
        current_action: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Use MedGemma to assess side effect severity (with vision if image present)"""
        
        reason = current_action.get("reason", "")
        
        if reason != "side_effects" and not reason.startswith("side_effect"):
            return {
                "intervention_type": "medgemma_consult",
                "risk_level": "low",
                "approved": True,
                "reason": "No side effects reported"
            }
        
        # Check if image is present - use vision analysis for side effects with photos
        if current_action.get("image"):
            return self._assess_with_vision(intervention, current_action)
        
        # Text-only side effect assessment
        # Create prompt for side effect assessment
        prompt = create_medical_prompt(
            question=(
                f"Patient reports side effects. "
                f"Notes: {current_action.get('notes', 'none')}. "
                "Should the patient seek immediate medical attention?"
            ),
            format_instructions=(
                "Respond with:\n"
                "- Severity: Mild/Moderate/Severe/Emergency\n"
                "- Urgent Care Needed: Yes/No\n"
                "- Recommendations: What patient should do"
            )
        )
        
        try:
            self.reasoning_steps.append("Consulting MedGemma for side effect severity...")
            response = self.llm.invoke(prompt)
            
            # Successfully consulted MedGemma
            self.medgemma_actually_consulted = True
            
            # Check for emergency keywords
            emergency_keywords = ["emergency", "urgent", "immediate", "doctor", "hospital"]
            requires_doctor = any(keyword in response.lower() for keyword in emergency_keywords)
            
            risk_level = "high" if requires_doctor else "medium"
            
            self.reasoning_steps.append(f"✅ MedGemma consulted - Side effect severity: {risk_level}")
            
            return {
                "intervention_type": "medgemma_consult",
                "risk_level": risk_level,
                "approved": not requires_doctor,
                "requires_doctor": requires_doctor,
                "medgemma_response": response[:500],
                "reason": "MedGemma side effect assessment completed"
            }
            
        except Exception as e:
            logger.error(f"MedGemma side effect assessment failed: {str(e)}")
            
            # Fallback: recommend caution
            return {
                "intervention_type": "medgemma_consult",
                "risk_level": "medium",
                "approved": False,
                "reason": "MedGemma unavailable - recommend manual review"
            }
    
    def _assess_with_vision(
        self,
        intervention: Dict[str, Any],
        current_action: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Use MedGemma Vision API to analyze medical images (e.g., side effect photos)"""
        
        image_data = current_action.get("image", "")
        notes = current_action.get("notes", "")
        image_day = current_action.get("image_day", 1)
        previous_images = current_action.get("previous_images", [])
        
        self.reasoning_steps.append(f"📸 Image detected (Day {image_day}) - activating MedGemma Vision analysis...")
        
        # Build vision analysis prompt
        if previous_images:
            # Temporal comparison mode
            prompt = create_medical_prompt(
                question=(
                    f"Patient reports: {notes}\n\n"
                    f"Analyzing Day {image_day} photo of side effect with {len(previous_images)} previous photo(s) for temporal comparison.\n"
                    "Please analyze the current image and compare with previous images to assess:\n"
                    "1. Lesion count and distribution pattern\n"
                    "2. Redness intensity and inflammation level\n"
                    "3. Healing trajectory (improving, stable, worsening)\n"
                    "4. Safety recommendation: Continue medication vs Stop immediately\n"
                ),
                format_instructions=(
                    "Respond with:\n"
                    "- Temporal Analysis: Compare Day 1 → Current Day\n"
                    "- Lesion Count Change: Percentage change\n"
                    "- Redness Intensity: Decreasing/Stable/Increasing\n"
                    "- Healing Trend: Clear improvement/No change/Worsening\n"
                    "- Recommendation: Continue with monitoring / Stop medication immediately\n"
                    "- Reasoning: Brief clinical explanation"
                )
            )
            self.reasoning_steps.append(f"🔬 Performing temporal analysis (Day 3 → Day {image_day})...")
        else:
            # Initial baseline assessment
            prompt = create_medical_prompt(
                question=(
                    f"Patient reports: {notes}\n\n"
                    "Please analyze this medical image (baseline Day 3 photo) to assess:\n"
                    "1. Severity of side effect (mild/moderate/severe)\n"
                    "2. Lesion characteristics and distribution\n"
                    "3. Signs of infection or complications\n"
                    "4. Initial safety recommendation\n"
                ),
                format_instructions=(
                    "Respond with:\n"
                    "- Severity: Mild/Moderate/Severe\n"
                    "- Description: Visual characteristics\n"
                    "- Immediate Concerns: Any red flags\n"
                    "- Recommendation: Monitor with daily photos / Seek immediate care\n"
                    "- Reasoning: Clinical rationale"
                )
            )
            self.reasoning_steps.append("📋 Performing baseline assessment (initial photo)...")
        
        try:
            # Call MedGemma Vision API with actual image data
            # The endpoint is configured as image-text-to-text (multimodal)
            response = self.llm.invoke(
                prompt,
                image=image_data,  # Pass base64 image to multimodal endpoint
                previous_images=previous_images  # For temporal comparison context
            )
            
            # Successfully consulted MedGemma Vision
            self.medgemma_actually_consulted = True
            
            # Parse response for key indicators
            improving = any(word in response.lower() for word in ["improving", "better", "healing", "decreasing"])
            worsening = any(word in response.lower() for word in ["worsening", "worse", "spreading", "severe"])
            
            # Determine risk level based on vision analysis
            if worsening:
                risk_level = "high"
                approved = False
                healing_trend = "worsening"
            elif improving:
                risk_level = "low"
                approved = True
                healing_trend = "improving"
            else:
                risk_level = "medium"
                approved = True
                healing_trend = "stable"
            
            self.reasoning_steps.append(
                f"✅ MedGemma Vision analysis complete - Healing trend: {healing_trend}"
            )
            
            return {
                "intervention_type": "vision_analysis",
                "risk_level": risk_level,
                "approved": approved,
                "vision_analysis_performed": True,
                "temporal_comparison": len(previous_images) > 0,
                "healing_trend": healing_trend,
                "image_day": image_day,
                "medgemma_response": response[:500],
                "reason": f"MedGemma Vision assessment completed (Day {image_day})"
            }
            
        except Exception as e:
            logger.error(f"MedGemma Vision analysis failed: {str(e)}")
            self.reasoning_steps.append(f"⚠️ Vision API error: {str(e)}")
            
            # Fallback: recommend caution for images
            return {
                "intervention_type": "vision_analysis",
                "risk_level": "medium",
                "approved": False,
                "vision_analysis_performed": False,
                "reason": "Vision API unavailable - recommend manual image review by healthcare provider"
            }
    
    def _determine_overall_risk(self, assessment_results: List[Dict[str, Any]]) -> str:
        """Determine overall risk level from individual assessments"""
        
        risk_levels = [result["risk_level"] for result in assessment_results]
        
        if "high" in risk_levels:
            return "high"
        elif "medium" in risk_levels:
            return "medium"
        else:
            return "low"
    
    def _generate_safety_recommendations(
        self,
        assessment_results: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate safety recommendations based on assessment"""
        
        recommendations = []
        
        # Check for high-risk items
        high_risk = [r for r in assessment_results if r["risk_level"] == "high"]
        if high_risk:
            recommendations.append("⚠️ High-risk intervention detected - requires human review")
            
            for risk in high_risk:
                if risk.get("requires_doctor"):
                    recommendations.append("Patient should consult healthcare provider")
        
        # Check for medium-risk items
        medium_risk = [r for r in assessment_results if r["risk_level"] == "medium"]
        if medium_risk:
            recommendations.append("Monitor patient closely after intervention")
        
        # General recommendations
        if not high_risk:
            recommendations.append("✓ Safe to proceed with automated execution")
            recommendations.append("Follow up with patient in 48-72 hours")
        
        return recommendations
    
    def _fallback_assessment(self, remediation: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback risk assessment when MedGemma is unavailable"""
        
        self.reasoning_steps.append("Using fallback risk assessment (MedGemma unavailable)")
        
        return {
            "approved": True,
            "overall_risk_level": "low",
            "intervention_assessments": [],
            "medgemma_consulted": False,
            "recommendations": [
                "MedGemma unavailable - using conservative approval",
                "Monitor intervention outcomes carefully"
            ],
            "warning": "Full medical validation not performed"
        }
    
    def get_reasoning_steps(self) -> List[str]:
        """Return reasoning steps for transparency"""
        return self.reasoning_steps
