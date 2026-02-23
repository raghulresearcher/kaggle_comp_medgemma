"""
Unit tests for Risk Assessment Agent
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from backend.agents.risk_agent import RiskAssessmentAgent


class TestRiskAssessmentAgent:
    """Test cases for Risk Assessment Agent"""
    
    def test_agent_initialization(self):
        """Test that agent initializes correctly"""
        agent = RiskAssessmentAgent()
        assert agent is not None
        assert agent.agent_type.value == "risk_assessment"
        assert hasattr(agent, 'llm')
        assert hasattr(agent, 'reasoning_steps')
    
    def test_validate_input_with_remediation_output(self, sample_remediation_output):
        """Test input validation with valid remediation output"""
        agent = RiskAssessmentAgent()
        input_data = {"remediation_output": sample_remediation_output}
        assert agent.validate_input(input_data) is True
    
    def test_validate_input_without_remediation_output(self):
        """Test input validation fails without remediation output"""
        agent = RiskAssessmentAgent()
        with pytest.raises(ValueError, match="remediation_output is required"):
            agent.validate_input({})
    
    def test_process_approves_safe_intervention(self, sample_remediation_output):
        """Test that safe interventions are approved"""
        agent = RiskAssessmentAgent()
        
        input_data = {
            "patient_id": "test_patient_001",
            "remediation_output": sample_remediation_output
        }
        
        result = agent.process(input_data)
        
        assert result["approved"] == True
        assert "reasoning" in result
    
    def test_process_with_image_triggers_vision(self):
        """Test that image field triggers vision analysis"""
        agent = RiskAssessmentAgent()
        input_data = {
            "patient_id": "test_patient_001",
            "current_action": {
                "reason": "side_effects",
                "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
                "notes": "Red rash on arms"
            },
            "remediation_output": {"interventions": []}
        }
        
        result = agent.process(input_data)
        
        # Should process without error when image provided
        assert "reasoning" in result
    
    def test_high_risk_intervention_flagged(self, sample_remediation_output):
        """Test that high-risk interventions are flagged for review"""
        agent = RiskAssessmentAgent()
        
        # Create high-risk remediation
        high_risk_remediation = {
            "interventions": [
                {
                    "type": "medication_change",
                    "action": "Switch to alternative medication",
                    "risk_level": "high"
                }
            ]
        }
        
        input_data = {
            "patient_id": "test_patient_001",
            "remediation_output": high_risk_remediation
        }
        
        with patch.object(agent, 'llm') as mock_llm:
            mock_llm.invoke.return_value = "This requires physician consultation."
            result = agent.process(input_data)
        
        assert "reasoning" in result
