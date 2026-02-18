"""
Learning Agent - Tracks outcomes and improves over time
"""
import logging
from typing import Any, Dict, List
from datetime import datetime, timedelta
from backend.agents.base_agent import BaseAgent, AgentType
from backend.firebase_client import adherence_service, intervention_service

logger = logging.getLogger(__name__)


class LearningAgent(BaseAgent):
    """
    Learns from intervention outcomes to improve future recommendations
    
    Responsibilities:
    - Track intervention effectiveness
    - Compare adherence before/after interventions
    - Identify successful patterns
    - Update success rates for different intervention types
    - Provide feedback to other agents
    """
    
    def __init__(self):
        super().__init__(AgentType.LEARNING)
        self.reasoning_steps = []
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input contains patient_id"""
        if "patient_id" not in input_data:
            raise ValueError("patient_id is required")
        return True
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Learn from current action and past interventions
        
        Args:
            input_data: Contains patient action and intervention history
            
        Returns:
            Learning insights and updated success metrics
        """
        self.reasoning_steps = []
        
        patient_id = input_data.get("patient_id")
        current_action = input_data.get("current_action", {})
        
        logger.info(f"Learning from outcomes for patient {patient_id}")
        self.reasoning_steps.append(f"📊 Learning Agent started for patient {patient_id}")
        self.reasoning_steps.append(f"🔍 Retrieving intervention history from Firestore...")
        
        # Get recent interventions
        interventions = intervention_service.get_patient_interventions(patient_id, limit=5)
        
        if not interventions:
            self.reasoning_steps.append("🆕 First intervention - establishing baseline")
            result = self._baseline_learning(patient_id, current_action)
            result["reasoning"] = self.reasoning_steps
            return result
        
        self.reasoning_steps.append(f"📚 Found {len(interventions)} previous interventions")
        self.reasoning_steps.append(f"📈 Calculating effectiveness metrics...")
        
        # Analyze intervention effectiveness
        effectiveness = self._analyze_intervention_effectiveness(patient_id, interventions)
        
        # Update learning model
        self.reasoning_steps.append("🧠 Generating insights from outcome data...")
        insights = self._generate_insights(effectiveness, interventions)
        
        # Provide recommendations for future interventions
        self.reasoning_steps.append("💡 Creating recommendations for future interventions...")
        recommendations = self._recommend_improvements(effectiveness, insights)
        
        self.reasoning_steps.append(f"✅ Learning cycle complete - {len(insights)} insights generated")
        self.reasoning_steps.append(f"📈 Model updated with effectiveness data")
        
        return {
            "learning_completed": True,
            "intervention_count": len(interventions),
            "effectiveness_analysis": effectiveness,
            "insights": insights,
            "recommendations": recommendations,
            "reasoning": self.reasoning_steps
        }
    
    def _baseline_learning(
        self,
        patient_id: str,
        current_action: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Initial learning when no interventions exist yet"""
        
        action = current_action.get("action")
        reason = current_action.get("reason")
        
        self.reasoning_steps.append(f"Recording baseline: {action} - {reason}")
        
        # Get baseline adherence
        try:
            baseline = adherence_service.calculate_adherence_rate(patient_id, days=7)
            
            self.reasoning_steps.append(
                f"Baseline adherence: {baseline.get('adherence_rate')}%"
            )
            
            return {
                "learning_completed": True,
                "type": "baseline",
                "baseline_adherence": baseline.get("adherence_rate"),
                "insights": [
                    f"Baseline established: {baseline.get('adherence_rate')}% adherence",
                    "Future interventions will be measured against this baseline"
                ],
                "recommendations": []
            }
            
        except Exception as e:
            logger.error(f"Baseline learning failed: {str(e)}")
            return {
                "learning_completed": False,
                "error": str(e)
            }
    
    def _analyze_intervention_effectiveness(
        self,
        patient_id: str,
        interventions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze how effective past interventions were"""
        
        self.reasoning_steps.append(f"Analyzing {len(interventions)} interventions")
        
        effectiveness_scores = []
        
        for intervention in interventions:
            intervention_date = intervention.get("created_at")
            root_cause = intervention.get("root_cause", "unknown")
            
            # Skip if intervention is too recent (less than 3 days)
            if intervention_date:
                try:
                    intervention_dt = intervention_date
                    days_since = (datetime.utcnow() - intervention_dt).days
                    
                    if days_since < 3:
                        self.reasoning_steps.append(
                            "Intervention too recent - skipping effectiveness analysis"
                        )
                        continue
                except:
                    pass
            
            # Compare adherence before and after intervention
            score = self._calculate_effectiveness_score(patient_id, intervention)
            effectiveness_scores.append({
                "root_cause": root_cause,
                "effectiveness_score": score,
                "intervention_date": str(intervention_date)
            })
        
        if not effectiveness_scores:
            return {
                "analyzed_count": 0,
                "message": "No interventions old enough to analyze"
            }
        
        # Calculate average effectiveness
        avg_score = sum(s["effectiveness_score"] for s in effectiveness_scores) / len(effectiveness_scores)
        
        self.reasoning_steps.append(f"Average intervention effectiveness: {avg_score:.2f}")
        
        return {
            "analyzed_count": len(effectiveness_scores),
            "average_effectiveness": round(avg_score, 2),
            "individual_scores": effectiveness_scores
        }
    
    def _calculate_effectiveness_score(
        self,
        patient_id: str,
        intervention: Dict[str, Any]
    ) -> float:
        """
        Calculate effectiveness score for a single intervention
        
        Score = (Adherence After - Adherence Before) / 100
        Range: -1.0 (made it worse) to +1.0 (perfect improvement)
        """
        
        try:
            intervention_date = intervention.get("created_at")
            
            if not intervention_date:
                return 0.0
            
            intervention_dt = intervention_date
            
            # Get adherence 7 days before intervention
            before_logs = adherence_service.get_patient_logs(patient_id, days=14)
            before_logs = [
                log for log in before_logs
                if datetime.fromisoformat(log.get("timestamp", "").replace('Z', '+00:00'))
                < intervention_dt
            ]
            
            # Get adherence 7 days after intervention
            after_logs = adherence_service.get_patient_logs(patient_id, days=7)
            after_logs = [
                log for log in after_logs
                if datetime.fromisoformat(log.get("timestamp", "").replace('Z', '+00:00'))
                >= intervention_dt
            ]
            
            # Calculate rates
            before_took = len([l for l in before_logs if l.get("action") == "took"])
            before_total = len(before_logs)
            before_rate = (before_took / before_total * 100) if before_total > 0 else 0
            
            after_took = len([l for l in after_logs if l.get("action") == "took"])
            after_total = len(after_logs)
            after_rate = (after_took / after_total * 100) if after_total > 0 else 0
            
            # Calculate improvement
            improvement = (after_rate - before_rate) / 100
            
            self.reasoning_steps.append(
                f"Adherence change: {before_rate:.1f}% → {after_rate:.1f}% "
                f"(+{improvement*100:.1f}%)"
            )
            
            return improvement
            
        except Exception as e:
            logger.error(f"Effectiveness calculation failed: {str(e)}")
            return 0.0
    
    def _generate_insights(
        self,
        effectiveness: Dict[str, Any],
        interventions: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate actionable insights from analysis"""
        
        insights = []
        
        avg_effectiveness = effectiveness.get("average_effectiveness", 0)
        
        if avg_effectiveness > 0.15:
            insights.append(
                f"✓ Interventions are highly effective (+{avg_effectiveness*100:.0f}% improvement)"
            )
            insights.append("Current approach is working well - continue similar strategies")
        
        elif avg_effectiveness > 0:
            insights.append(
                f"Interventions show modest improvement (+{avg_effectiveness*100:.0f}%)"
            )
            insights.append("Consider more aggressive intervention strategies")
        
        else:
            insights.append("⚠️ Interventions not showing expected improvement")
            insights.append("Recommend reviewing intervention approach")
        
        # Analyze patterns by root cause
        individual_scores = effectiveness.get("individual_scores", [])
        if individual_scores:
            by_cause = {}
            for score in individual_scores:
                cause = score["root_cause"]
                if cause not in by_cause:
                    by_cause[cause] = []
                by_cause[cause].append(score["effectiveness_score"])
            
            # Find most effective intervention type
            cause_avg = {
                cause: sum(scores) / len(scores)
                for cause, scores in by_cause.items()
            }
            
            best_cause = max(cause_avg, key=cause_avg.get, default=None)
            if best_cause:
                insights.append(
                    f"Most effective interventions target: {best_cause}"
                )
        
        self.reasoning_steps.append(f"Generated {len(insights)} insights")
        
        return insights
    
    def _recommend_improvements(
        self,
        effectiveness: Dict[str, Any],
        insights: List[str]
    ) -> List[Dict[str, str]]:
        """Recommend improvements for future interventions"""
        
        recommendations = []
        
        avg_effectiveness = effectiveness.get("average_effectiveness", 0)
        
        if avg_effectiveness < 0.05:
            recommendations.append({
                "priority": "high",
                "recommendation": "Current interventions not effective",
                "action": "Try different intervention types or increase intensity"
            })
        
        if avg_effectiveness > 0.15:
            recommendations.append({
                "priority": "low",
                "recommendation": "Maintain current approach",
                "action": "Continue monitoring - interventions are working well"
            })
        
        # Check for specific patterns
        individual_scores = effectiveness.get("individual_scores", [])
        if len(individual_scores) >= 3:
            recent_scores = [s["effectiveness_score"] for s in individual_scores[:3]]
            if all(score > 0.1 for score in recent_scores):
                recommendations.append({
                    "priority": "medium",
                    "recommendation": "Consistent success pattern detected",
                    "action": "Patient responding well - consider reducing intervention frequency"
                })
        
        self.reasoning_steps.append(f"Generated {len(recommendations)} recommendations")
        
        return recommendations
    
    def get_reasoning_steps(self) -> List[str]:
        """Return reasoning steps for transparency"""
        return self.reasoning_steps
