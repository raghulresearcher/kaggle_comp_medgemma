"""
Initialize and register all agents with the orchestrator
This module should be imported by app.py to set up the agent system
"""
import logging
from backend.agents.base_agent import orchestrator
from backend.agents.investigation_agent import InvestigationAgent
from backend.agents.remediation_agent import RemediationAgent
from backend.agents.risk_agent import RiskAssessmentAgent
from backend.agents.execution_agent import ExecutionAgent
from backend.agents.learning_agent import LearningAgent

logger = logging.getLogger(__name__)


def initialize_agents():
    """
    Initialize and register all agents with the orchestrator
    Call this function once at application startup
    """
    logger.info("Initializing agent system...")
    
    try:
        # Create agent instances
        investigation_agent = InvestigationAgent()
        remediation_agent = RemediationAgent()
        risk_agent = RiskAssessmentAgent()
        execution_agent = ExecutionAgent()
        learning_agent = LearningAgent()
        
        # Register with orchestrator
        orchestrator.register_agent(investigation_agent)
        orchestrator.register_agent(remediation_agent)
        orchestrator.register_agent(risk_agent)
        orchestrator.register_agent(execution_agent)
        orchestrator.register_agent(learning_agent)
        
        logger.info(f"✓ Registered {len(orchestrator.agents)} agents")
        logger.info("Agent system initialized successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize agent system: {str(e)}")
        raise


# Initialize agents when this module is imported
initialize_agents()
