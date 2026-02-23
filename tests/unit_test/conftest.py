"""
Pytest configuration and shared fixtures for unit tests
"""
import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def sample_patient_data():
    """Sample patient data for testing"""
    return {
        "patient_id": "test_patient_001",
        "action": "took",
        "medication_id": "med_test_100mg",
        "timestamp": "2026-02-23T10:00:00Z",
        "reason": "scheduled"
    }


@pytest.fixture
def sample_adherence_logs():
    """Sample adherence logs for testing"""
    return [
        {
            "patient_id": "test_patient_001",
            "action": "took",
            "medication_id": "med_test_100mg",
            "timestamp": "2026-02-20T08:00:00Z"
        },
        {
            "patient_id": "test_patient_001",
            "action": "skipped",
            "medication_id": "med_test_100mg",
            "timestamp": "2026-02-21T08:00:00Z",
            "reason": "forgot"
        },
        {
            "patient_id": "test_patient_001",
            "action": "took",
            "medication_id": "med_test_100mg",
            "timestamp": "2026-02-22T08:00:00Z"
        }
    ]


@pytest.fixture
def sample_investigation_output():
    """Sample investigation agent output"""
    return {
        "pattern_detected": True,
        "root_cause": "timing_conflict",
        "adherence_rate": 75.0,
        "total_actions": 20,
        "skipped_count": 5,
        "pattern_details": {
            "issue": "Morning medication timing confusion",
            "frequency": "3x per week"
        }
    }


@pytest.fixture
def sample_remediation_output():
    """Sample remediation agent output"""
    return {
        "plan_type": "targeted",
        "interventions": [
            {
                "type": "schedule_adjustment",
                "action": "Create simplified morning schedule",
                "timing": "6:30 AM - Thyroid, 7:30 AM - Breakfast + Metformin"
            }
        ],
        "expected_improvement": "20-30% adherence increase"
    }


@pytest.fixture
def mock_medgemma_response():
    """Mock MedGemma API response"""
    return {
        "generated_text": "Based on the medication timing requirements, "
                         "the recommended schedule is medically appropriate. "
                         "Levothyroxine should be taken 1 hour before food, "
                         "followed by breakfast with Metformin."
    }
