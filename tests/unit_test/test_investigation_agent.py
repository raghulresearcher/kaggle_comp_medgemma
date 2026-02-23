"""
Unit tests for Investigation Agent
"""
import pytest
from unittest.mock import Mock, patch
from backend.agents.investigation_agent import InvestigationAgent


class TestInvestigationAgent:
    """Test cases for Investigation Agent"""
    
    def test_agent_initialization(self):
        """Test that agent initializes correctly"""
        agent = InvestigationAgent()
        assert agent is not None
        assert agent.agent_type.value == "investigation"
        assert hasattr(agent, 'llm')
        assert hasattr(agent, 'reasoning_steps')
    
    def test_validate_input_with_patient_id(self, sample_patient_data):
        """Test input validation with valid patient_id"""
        agent = InvestigationAgent()
        assert agent.validate_input(sample_patient_data) is True
    
    def test_validate_input_without_patient_id(self):
        """Test input validation fails without patient_id"""
        agent = InvestigationAgent()
        with pytest.raises(ValueError, match="patient_id is required"):
            agent.validate_input({})
    
    @patch('backend.agents.investigation_agent.adherence_service')
    def test_process_with_no_logs(self, mock_service, sample_patient_data):
        """Test processing when no adherence logs exist"""
        mock_service.get_patient_logs.return_value = []
        
        agent = InvestigationAgent()
        result = agent.process(sample_patient_data)
        
        assert result["pattern_detected"] is False
        assert result["message"] == "Insufficient data for pattern analysis"
        assert "reasoning" in result
    
    @patch('backend.agents.investigation_agent.adherence_service')
    def test_process_with_good_adherence(self, mock_service, sample_patient_data):
        """Test processing with good adherence (few skips)"""
        # Mock 10 logs with only 1 skip (90% adherence)
        mock_logs = [{"action": "took"} for _ in range(9)] + [{"action": "skipped"}]
        mock_service.get_patient_logs.return_value = mock_logs
        
        agent = InvestigationAgent()
        result = agent.process(sample_patient_data)
        
        assert result["pattern_detected"] is False
        assert result["adherence_rate"] == 90.0
        assert result["skipped_count"] == 1
    
    @patch('backend.agents.investigation_agent.adherence_service')
    def test_process_detects_timing_conflict(self, mock_service, sample_patient_data):
        """Test that agent detects timing conflict pattern"""
        # Mock logs with timing conflict pattern
        mock_logs = [
            {"action": "skipped", "reason": "timing_conflict", "timestamp": "2026-02-20T08:00:00Z"},
            {"action": "took", "timestamp": "2026-02-21T08:00:00Z"},
            {"action": "skipped", "reason": "timing_conflict", "timestamp": "2026-02-22T08:00:00Z"},
            {"action": "took", "timestamp": "2026-02-23T08:00:00Z"}
        ]
        mock_service.get_patient_logs.return_value = mock_logs
        
        agent = InvestigationAgent()
        result = agent.process(sample_patient_data)
        
        assert result["pattern_detected"] is True
        assert result["adherence_rate"] == 50.0
        assert "reasoning" in result
    
    def test_reasoning_steps_populated(self, sample_patient_data):
        """Test that reasoning steps are captured during processing"""
        agent = InvestigationAgent()
        with patch('backend.agents.investigation_agent.adherence_service') as mock_service:
            mock_service.get_patient_logs.return_value = []
            result = agent.process(sample_patient_data)
        
        assert len(result["reasoning"]) > 0
        assert any("Investigation Agent started" in step for step in result["reasoning"])
