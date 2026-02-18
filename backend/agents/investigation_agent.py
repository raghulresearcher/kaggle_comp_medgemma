"""
Investigation Agent - Analyzes patterns and identifies root causes
"""
import logging
from typing import Any, Dict, List
from datetime import datetime, timedelta
from collections import Counter
from backend.agents.base_agent import BaseAgent, AgentType
from backend.firebase_client import adherence_service, patient_service

logger = logging.getLogger(__name__)


class InvestigationAgent(BaseAgent):
    """
    Investigates medication adherence patterns to identify root causes

    Responsibilities:
    - Analyze adherence history for patterns
    - Identify specific times/days with issues
    - Determine root causes (forgot, ran out, side effects)
    - Provide detailed analysis for remediation
    """

    def __init__(self):
        super().__init__(AgentType.INVESTIGATION)
        self.reasoning_steps = []

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data contains patient_id"""
        if "patient_id" not in input_data:
            raise ValueError("patient_id is required")
        return True

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze adherence patterns and identify issues

        Args:
            input_data: Contains patient_id, action, reason, etc.

        Returns:
            Analysis results with identified patterns
        """
        self.reasoning_steps = []
        patient_id = input_data["patient_id"]

        logger.info(f"Investigating patterns for patient {patient_id}")
        self.reasoning_steps.append(f"🔍 Investigation Agent started for patient {patient_id}")
        self.reasoning_steps.append(f"📊 Retrieving last 30 days of adherence data from Firestore...")

        # Get adherence logs (last 30 days)
        logs = adherence_service.get_patient_logs(patient_id, days=30)

        if not logs:
            logger.warning(f"No adherence logs found for patient {patient_id}")
            self.reasoning_steps.append("ℹ️ No historical data found - insufficient for pattern analysis")
            return {
                "pattern_detected": False,
                "message": "Insufficient data for pattern analysis",
                "reasoning": self.reasoning_steps
            }

        self.reasoning_steps.append(f"✅ Retrieved {len(logs)} adherence records")
        
        # Analyze skipped doses
        skipped_logs = [log for log in logs if log.get("action") == "skipped"]
        adherence_rate = round((len(logs) - len(skipped_logs)) / len(logs) * 100, 2) if logs else 0
        
        self.reasoning_steps.append(f"📈 Analysis: {len(logs)} total doses, {len(skipped_logs)} skipped ({100-adherence_rate:.1f}% miss rate)")
        
        if len(skipped_logs) < 2:
            self.reasoning_steps.append("✓ Good adherence - not enough misses to identify concerning pattern")
            analysis = {
                "pattern_detected": False,
                "total_actions": len(logs),
                "skipped_count": len(skipped_logs),
                "adherence_rate": adherence_rate,
                "reasoning": self.reasoning_steps
            }
        else:
            self.reasoning_steps.append("🔎 Analyzing temporal patterns...")
            
            # Analyze patterns
            day_pattern = self._analyze_day_pattern(skipped_logs)
            time_pattern = self._analyze_time_pattern(skipped_logs)
            reason_pattern = self._analyze_reasons(skipped_logs)
            
            self.reasoning_steps.append("🧠 Identifying root cause...")
            root_cause = self._determine_root_cause(day_pattern, time_pattern, reason_pattern)
            
            analysis = {
                "pattern_detected": True,
                "total_actions": len(logs),
                "skipped_count": len(skipped_logs),
                "adherence_rate": adherence_rate,
                "day_pattern": day_pattern,
                "time_pattern": time_pattern,
                "reason_pattern": reason_pattern,
                "root_cause": root_cause,
                "recommendations": self._generate_recommendations(root_cause),
                "reasoning": self.reasoning_steps
            }

        # Add current action context
        analysis["current_action"] = {
            "action": input_data.get("action"),
            "reason": input_data.get("reason"),
            "timestamp": input_data.get("timestamp")
        }
        
        # CRITICAL: Override for side effects - requires medical assessment
        current_reason = input_data.get("reason")
        if current_reason == "side_effects":
            self.reasoning_steps.append("⚠️ SIDE EFFECTS DETECTED - Prioritizing medical assessment")
            analysis["root_cause"] = "Tolerability issue: Side effects affecting adherence"
            analysis["recommendations"] = [
                "Consult MedGemma for side effect severity assessment",
                "Consider dosage adjustment or timing change",
                "Evaluate medication tolerance"
            ]
            analysis["pattern_detected"] = True  # Force full workflow
            analysis["reasoning"] = self.reasoning_steps
        
        return analysis

    def _analyze_day_pattern(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze which days of week have issues"""
        days = []

        for log in logs:
            timestamp_str = log.get("timestamp", "")
            if timestamp_str:
                try:
                    dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    days.append(dt.strftime("%A"))  # Day name
                except:
                    pass

        if not days:
            return {"problem_day": None}

        day_counts = Counter(days)
        most_common = day_counts.most_common(1)

        if most_common:
            problem_day = most_common[0][0]
            count = most_common[0][1]

            self.reasoning_steps.append(f"📅 Day pattern: {count} skips on {problem_day}s (recurring weekly pattern)")

            return {
                "problem_day": problem_day,
                "occurrences": count,
                "pattern_strength": "strong" if count >= 3 else "weak"
            }

        return {"problem_day": None}

    def _analyze_time_pattern(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze which times of day have issues"""
        times = []

        for log in logs:
            timestamp_str = log.get("timestamp", "")
            if timestamp_str:
                try:
                    dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    hour = dt.hour

                    if 5 <= hour < 12:
                        times.append("morning")
                    elif 12 <= hour < 17:
                        times.append("afternoon")
                    elif 17 <= hour < 21:
                        times.append("evening")
                    else:
                        times.append("night")
                except:
                    pass

        if not times:
            return {"problem_time": None}

        time_counts = Counter(times)
        most_common = time_counts.most_common(1)

        if most_common:
            problem_time = most_common[0][0]
            count = most_common[0][1]

            self.reasoning_steps.append(f"⏰ Time pattern: {count} skips in {problem_time} (consistent timing issue)")

            return {
                "problem_time": problem_time,
                "occurrences": count,
                "pattern_strength": "strong" if count >= 3 else "weak"
            }

        return {"problem_time": None}

    def _analyze_reasons(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze stated reasons for skipping"""
        reasons = [log.get("reason", "unknown") for log in logs]
        reason_counts = Counter(reasons)

        reason_str = ", ".join([f"{k}: {v}" for k, v in reason_counts.items()])
        self.reasoning_steps.append(f"💬 Stated reasons: {reason_str}")

        most_common = reason_counts.most_common(1)

        if most_common:
            primary_reason = most_common[0][0]
            count = most_common[0][1]

            return {
                "primary_reason": primary_reason,
                "occurrences": count,
                "all_reasons": dict(reason_counts)
            }

        return {"primary_reason": "unknown"}

    def _determine_root_cause(
        self,
        day_pattern: Dict[str, Any],
        time_pattern: Dict[str, Any],
        reason_pattern: Dict[str, Any]
    ) -> str:
        """Determine the primary root cause"""

        primary_reason = reason_pattern.get("primary_reason", "unknown")

        # Check for behavioral patterns
        if day_pattern.get("problem_day") and day_pattern.get("pattern_strength") == "strong":
            root_cause = f"Behavioral pattern: Consistently forgets on {day_pattern['problem_day']}"
            self.reasoning_steps.append(f"✓ ROOT CAUSE: {root_cause}")
            return root_cause

        if time_pattern.get("problem_time") and time_pattern.get("pattern_strength") == "strong":
            root_cause = f"Timing issue: Consistently forgets during {time_pattern['problem_time']}"
            self.reasoning_steps.append(f"Root cause identified: {root_cause}")
            return root_cause

        # Reason-based root cause
        if primary_reason == "forgot":
            root_cause = "Memory/reminder issue: Patient frequently forgets"
        elif primary_reason == "ran_out":
            root_cause = "Supply chain issue: Medication running out"
        elif primary_reason == "side_effects":
            root_cause = "Tolerability issue: Side effects affecting adherence"
        else:
            root_cause = "Unknown: Pattern unclear, needs more data"

        self.reasoning_steps.append(f"Root cause identified: {root_cause}")
        return root_cause

    def _generate_recommendations(self, root_cause: str) -> List[str]:
        """Generate recommendations based on root cause"""

        recommendations = []

        if "Behavioral pattern" in root_cause or "Timing issue" in root_cause:
            recommendations.append("Adjust reminder time to better fit patient's schedule")
            recommendations.append("Add contextual reminder (e.g., 'with breakfast')")

        elif "Memory/reminder" in root_cause:
            recommendations.append("Increase reminder frequency")
            recommendations.append("Add follow-up reminder if first is missed")

        elif "Supply chain" in root_cause:
            recommendations.append("Set up auto-refill")
            recommendations.append("Add refill reminder 7 days before running out")

        elif "Tolerability" in root_cause:
            recommendations.append("Consult MedGemma for side effect management")
            recommendations.append("Suggest timing adjustment (e.g., with food)")

        else:
            recommendations.append("Continue monitoring for clearer pattern")

        self.reasoning_steps.append(f"Generated {len(recommendations)} recommendations")

        return recommendations

    def get_reasoning_steps(self) -> List[str]:
        """Return reasoning steps for transparency"""
        return self.reasoning_steps
