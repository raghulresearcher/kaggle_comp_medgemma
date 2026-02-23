"""
Unit tests for Remediation Agent
"""
import pytest
from unittest.mock import Mock, patch
from backend.agents.remediation_agent import RemediationAgent


class TestRemediationAgent:
    """Test cases for Remediation Agent"""
    
    def test_agent_initialization(self):
        """Test that agent initializes correctly"""
        agent = RemediationAgent()
        assert agent is not None
        assert agent.agent_type.value == "remediation"
        assert hasattr(agent, 'llm')
        assert hasattr(agent, 'reasoning_steps')
    
    def test_validate_input_with_investigation_output(self, sample_investigation_output):
        """Test input validation with valid investigation output"""
        agent = RemediationAgent()
        input_data = {"investigation_output": sample_investigation_output}
        assert agent.validate_input(input_data) is True
    
    def test_validate_input_without_investigation_output(self):
        """Test input validation fails without investigation output"""
        agent = RemediationAgent()
        with pytest.raises(ValueError, match="investigation_output is required"):
            agent.validate_input({})
    
    def test_process_with_no_pattern(self, sample_patient_data):
        """Test processing when no pattern detected"""
        agent = RemediationAgent()
        input_data = {
            "patient_id": "test_patient_001",
            "investigation_output": {"pattern_detected": False}
        }
        
        result = agent.process(input_data)
        
        assert result["plan_type"] == "general"
        assert "interventions" in result
        assert "reasoning" in result
    
    def test_process_with_timing_conflict(self, sample_investigation_output):
        """Test remediation plan for timing conflict"""
        agent = RemediationAgent()
        input_data = {
            "patient_id": "test_patient_001",
            "investigation_output": sample_investigation_output
        }
        
        result = agent.process(input_data)
        
        assert result["plan_type"] == "targeted"
        assert "interventions" in result
        assert len(result["interventions"]) > 0
        assert "reasoning" in result
    
    def test_process_with_side_effects(self):
        """Test remediation plan for side effects"""
        agent = RemediationAgent()
        investigation_output = {
            "pattern_detected": True,
            "root_cause": "side_effects",
            "adherence_rate": 60.0
        }
        input_data = {
            "patient_id": "test_patient_001",
            "investigation_output": investigation_output
        }
        
        result = agent.process(input_data)
        
        assert result["plan_type"] == "targeted"
        # Verify remediation includes some intervention
        assert len(result["interventions"]) > 0
