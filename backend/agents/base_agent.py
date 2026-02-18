"""
Base Agent Class and Agent Orchestrator
Core framework for the 5-agent agentic workflow
"""
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


# ============================================================================
# Agent Types and Workflow States
# ============================================================================

class AgentType(Enum):
    """Types of specialized agents in the system"""
    INVESTIGATION = "investigation"
    REMEDIATION = "remediation"
    RISK_ASSESSMENT = "risk_assessment"
    EXECUTION = "execution"
    LEARNING = "learning"


class WorkflowState(Enum):
    """States of agent workflow execution"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    REQUIRES_HUMAN = "requires_human"


# ============================================================================
# Base Agent Class
# ============================================================================

class BaseAgent(ABC):
    """
    Abstract base class for all specialized agents
    
    Each agent must implement:
    - process(): Main logic for the agent's task
    - validate_input(): Ensure input data is valid
    - format_output(): Structure the agent's results
    """
    
    def __init__(self, agent_type: AgentType):
        self.agent_type = agent_type
        self.name = agent_type.value
        self.execution_history: List[Dict[str, Any]] = []
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main processing logic for the agent
        
        Args:
            input_data: Input data for the agent to process
            
        Returns:
            Agent's output/results
        """
        pass
    
    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        Validate that input data is correct for this agent
        
        Args:
            input_data: Input data to validate
            
        Returns:
            True if valid, raises ValueError otherwise
        """
        pass
    
    def format_output(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format the agent's output with metadata
        
        Args:
            result: Raw result from processing
            
        Returns:
            Formatted output with metadata
        """
        return {
            "agent": self.name,
            "agent_type": self.agent_type.value,
            "timestamp": datetime.utcnow().isoformat(),
            "result": result
        }
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent with logging and error handling
        
        Args:
            input_data: Input data for processing
            
        Returns:
            Formatted output
        """
        try:
            logger.info(f"{self.name} agent started")
            
            # Validate input
            if not self.validate_input(input_data):
                raise ValueError(f"Invalid input for {self.name} agent")
            
            # Process
            start_time = datetime.utcnow()
            result = self.process(input_data)
            end_time = datetime.utcnow()
            
            # Format output
            output = self.format_output(result)
            output["execution_time_ms"] = int((end_time - start_time).total_seconds() * 1000)
            output["status"] = "success"
            
            # Log execution
            self.execution_history.append(output)
            logger.info(f"{self.name} agent completed successfully")
            
            return output
            
        except Exception as e:
            logger.error(f"{self.name} agent failed: {str(e)}")
            
            error_output = {
                "agent": self.name,
                "agent_type": self.agent_type.value,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "error",
                "error": str(e)
            }
            
            self.execution_history.append(error_output)
            return error_output
    
    def get_reasoning_steps(self) -> List[str]:
        """
        Get list of reasoning steps for transparency
        Override in subclasses for specific reasoning
        
        Returns:
            List of reasoning step descriptions
        """
        return [f"{self.name} agent executed"]


# ============================================================================
# Agent Orchestrator
# ============================================================================

class AgentOrchestrator:
    """
    Orchestrates the 5-agent workflow for medication adherence
    
    Workflow:
    1. Investigation Agent - Analyzes patterns and identifies root cause
    2. Remediation Agent - Proposes solutions
    3. Risk Assessment Agent - Validates safety with MedGemma
    4. Execution Agent - Implements the solution
    5. Learning Agent - Tracks outcomes for improvement
    """
    
    def __init__(self):
        self.agents: Dict[AgentType, BaseAgent] = {}
        self.workflow_history: List[Dict[str, Any]] = []
        self.active_workflows: Dict[str, Dict[str, Any]] = {}  # For real-time tracking
    
    def register_agent(self, agent: BaseAgent):
        """
        Register an agent with the orchestrator
        
        Args:
            agent: Agent instance to register
        """
        self.agents[agent.agent_type] = agent
        logger.info(f"Registered {agent.name} agent")
    
    def get_agent(self, agent_type: AgentType) -> Optional[BaseAgent]:
        """
        Get a registered agent by type
        
        Args:
            agent_type: Type of agent to retrieve
            
        Returns:
            Agent instance or None
        """
        return self.agents.get(agent_type)
    
    def execute_workflow(
        self,
        trigger_data: Dict[str, Any],
        agents_to_run: Optional[List[AgentType]] = None
    ) -> Dict[str, Any]:
        """
        Execute the full agent workflow or specific agents
        
        Args:
            trigger_data: Initial data that triggered the workflow
            agents_to_run: Specific agents to run (or None for full workflow)
            
        Returns:
            Workflow results with all agent outputs
        """
        workflow_id = f"wf_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        logger.info(f"Starting workflow {workflow_id}")
        
        # Default to full workflow
        if agents_to_run is None:
            agents_to_run = [
                AgentType.INVESTIGATION,
                AgentType.REMEDIATION,
                AgentType.RISK_ASSESSMENT,
                AgentType.EXECUTION,
                AgentType.LEARNING
            ]
        
        workflow_result = {
            "workflow_id": workflow_id,
            "trigger": trigger_data,
            "started_at": datetime.utcnow().isoformat(),
            "agents_executed": [],
            "reasoning_trace": [],  # Collect all reasoning steps
            "state": WorkflowState.IN_PROGRESS.value
        }
        
        # Execute agents in sequence
        previous_output = trigger_data
        
        for agent_type in agents_to_run:
            agent = self.get_agent(agent_type)
            
            if not agent:
                logger.warning(f"Agent {agent_type.value} not registered, skipping")
                continue
            
            # Execute agent with previous output as input
            agent_result = agent.execute(previous_output)
            workflow_result["agents_executed"].append(agent_result)
            
            # Collect reasoning steps from agent if available
            if "result" in agent_result and "reasoning" in agent_result["result"]:
                reasoning_steps = agent_result["result"]["reasoning"]
                workflow_result["reasoning_trace"].extend(reasoning_steps)
            
            # Check if agent failed
            if agent_result.get("status") == "error":
                logger.error(f"Workflow {workflow_id} failed at {agent_type.value}")
                workflow_result["state"] = WorkflowState.FAILED.value
                workflow_result["failed_at_agent"] = agent_type.value
                break
            
            # Use this agent's output as input for next agent
            previous_output = {
                **previous_output,
                f"{agent_type.value}_output": agent_result.get("result", {})
            }
        
        # Mark workflow as completed if no failures
        if workflow_result["state"] == WorkflowState.IN_PROGRESS.value:
            workflow_result["state"] = WorkflowState.COMPLETED.value
        
        workflow_result["completed_at"] = datetime.utcnow().isoformat()
        
        # Store workflow in active_workflows for SSE streaming
        self.active_workflows[workflow_id] = workflow_result
        
        # Store in history
        self.workflow_history.append(workflow_result)
        
        logger.info(f"Workflow {workflow_id} completed with state: {workflow_result['state']}")
        logger.info(f"Collected {len(workflow_result['reasoning_trace'])} reasoning steps")
        
        # Generate summary of the workflow
        workflow_result["summary"] = self._generate_workflow_summary(workflow_result)
        
        return workflow_result
    
    def _generate_workflow_summary(self, workflow_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate an intelligent, conversational summary of the workflow
        
        Args:
            workflow_result: Complete workflow result
            
        Returns:
            Rich summary dict with narrative and insights
        """
        agents_executed = workflow_result.get("agents_executed", [])
        reasoning_trace = workflow_result.get("reasoning_trace", [])
        
        # Extract detailed information from each agent
        investigation_data = {}
        remediation_data = {}
        risk_data = {}
        execution_data = {}
        learning_data = {}
        
        for agent in agents_executed:
            agent_type = agent.get("agent_type", "")
            result = agent.get("result", {})
            
            if agent_type == "investigation":
                investigation_data = result
            elif agent_type == "remediation":
                remediation_data = result
            elif agent_type == "risk_assessment":
                risk_data = result
            elif agent_type == "execution":
                execution_data = result
            elif agent_type == "learning":
                learning_data = result
        
        # Count key metrics
        total_steps = len(reasoning_trace)
        medgemma_consultations = sum(1 for agent in agents_executed 
                                     if agent.get("result", {}).get("medgemma_consulted", False))
        
        # Extract key insights
        pattern_detected = investigation_data.get("pattern_detected", False)
        root_cause = investigation_data.get("root_cause", "")
        adherence_rate = investigation_data.get("adherence_rate", 0)
        
        interventions = remediation_data.get("interventions", [])
        intervention_types = [i.get("type", "") for i in interventions]
        
        risk_level = risk_data.get("overall_risk_level", "Unknown")
        risk_approved = risk_data.get("approved", False)
        
        executed_actions = execution_data.get("executed_actions", [])
        
        # Generate conversational narrative
        action = workflow_result.get("trigger", {}).get("action", "unknown")
        reason = workflow_result.get("trigger", {}).get("reason", "unknown").replace("_", " ")
        patient_id = workflow_result.get("trigger", {}).get("patient_id", "unknown")
        
        # Build story-like summary
        story_parts = []
        
        # Opening
        if action == "skipped":
            story_parts.append(f"🚨 Patient {patient_id} skipped their medication because they {reason}.")
        elif action == "took":
            story_parts.append(f"✅ Patient {patient_id} took their medication but reported {reason}.")
        
        # Investigation insights
        if pattern_detected:
            story_parts.append(f"🔍 Analysis revealed a pattern: {root_cause}")
            if adherence_rate > 0:
                story_parts.append(f"Current adherence rate is {adherence_rate}%.")
        else:
            story_parts.append("🔍 No recurring pattern detected - appears to be an isolated incident.")
        
        # Remediation
        if interventions:
            story_parts.append(f"💡 System designed {len(interventions)} personalized intervention(s): {', '.join(intervention_types[:3])}.")
        
        # Risk assessment
        if risk_level != "Unknown":
            risk_emoji = {"low": "✅", "medium": "⚠️", "high": "🚨", "critical": "🔴"}.get(risk_level.lower(), "❓")
            story_parts.append(f"{risk_emoji} Medical safety check assessed risk as {risk_level.upper()}.")
            if not risk_approved:
                story_parts.append("⚠️ Physician review recommended before proceeding.")
        
        # MedGemma consultation
        if medgemma_consultations > 0:
            story_parts.append(f"🧠 MedGemma medical AI was consulted {medgemma_consultations} time(s) for clinical validation.")
        
        # Execution
        if executed_actions:
            story_parts.append(f"⚡ Implemented {len(executed_actions)} action(s) automatically.")
        
        summary_text = " ".join(story_parts)
        
        # Extract specific findings and recommendations
        findings = []
        if root_cause:
            findings.append(root_cause)
        if adherence_rate < 80 and adherence_rate > 0:
            findings.append(f"Below-target adherence at {adherence_rate}%")
        
        recommendations = []
        for intervention in interventions[:3]:
            if intervention.get("action"):
                recommendations.append(intervention["action"])
        
        insights = []
        if pattern_detected:
            insights.append("Recurring behavioral pattern identified")
        if medgemma_consultations > 0:
            insights.append("Medical AI validated safety and appropriateness")
        if risk_approved:
            insights.append("All interventions cleared for automated execution")
        
        return {
            "summary_text": summary_text,
            "key_findings": findings if findings else ["No significant issues identified"],
            "recommended_actions": recommendations if recommendations else ["Monitoring and support"],
            "risk_level": risk_level if risk_level != "Unknown" else "Low",
            "risk_approved": risk_approved,
            "execution_status": "Completed" if executed_actions else "Pending",
            "learning_insights": insights,
            "total_reasoning_steps": total_steps,
            "medgemma_consultations": medgemma_consultations,
            "agents_completed": len([a for a in agents_executed if a.get("status") == "success"]),
            "total_agents": len(agents_executed),
            "adherence_rate": adherence_rate,
            "pattern_detected": pattern_detected,
            "interventions_count": len(interventions)
        }
    
    def route_patient_action(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route a patient action to the appropriate workflow
        
        Args:
            action_data: Patient action data
            
        Returns:
            Workflow result
        """
        action = action_data.get("action")
        reason = action_data.get("reason")
        
        logger.info(f"Routing patient action: {action} - {reason}")
        
        # Determine which agents to run based on action and reason
        if action == "skipped":
            # Check if medical reasoning (MedGemma) is needed
            if reason in ["timing_conflict", "supplement_interference"]:
                # Full workflow with MedGemma for complex medical decisions
                return self.execute_workflow(action_data)
            else:
                # Full workflow for other skipped doses
                return self.execute_workflow(action_data)
        
        elif action == "took":
            # Check if this is a side effects concern
            if reason == "side_effects":
                # Full workflow for side effects - medical assessment needed
                return self.execute_workflow(action_data)
            else:
                # Just learning agent for routine successful doses
                return self.execute_workflow(action_data, agents_to_run=[AgentType.LEARNING])
        
        elif action == "snoozed":
            # Investigation + Learning
            return self.execute_workflow(
                action_data,
                agents_to_run=[AgentType.INVESTIGATION, AgentType.LEARNING]
            )
        
        else:
            logger.warning(f"Unknown action type: {action}")
            return {
                "status": "error",
                "message": f"Unknown action type: {action}"
            }
    
    def get_reasoning_trace(self, workflow_id: str) -> Dict[str, Any]:
        """
        Get detailed reasoning trace for a workflow (for transparency)
        
        Args:
            workflow_id: Workflow identifier
            
        Returns:
            Detailed reasoning steps from all agents
        """
        # Find workflow in history
        workflow = next(
            (wf for wf in self.workflow_history if wf["workflow_id"] == workflow_id),
            None
        )
        
        if not workflow:
            return {"error": "Workflow not found"}
        
        # Compile reasoning from all agents
        reasoning = {
            "workflow_id": workflow_id,
            "trigger": workflow["trigger"],
            "steps": []
        }
        
        for agent_result in workflow.get("agents_executed", []):
            agent_type = agent_result.get("agent_type")
            agent = self.get_agent(AgentType(agent_type))
            
            if agent:
                reasoning["steps"].append({
                    "agent": agent_type,
                    "timestamp": agent_result.get("timestamp"),
                    "reasoning": agent.get_reasoning_steps(),
                    "result": agent_result.get("result", {})
                })
        
        return reasoning


# ============================================================================
# Global Orchestrator Instance
# ============================================================================

# Singleton orchestrator
orchestrator = AgentOrchestrator()



