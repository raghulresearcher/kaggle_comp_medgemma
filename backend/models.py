"""
Data Models for Firestore Collections
Defines the structure of data stored in Firebase
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


# ============================================================================
# Patient Models
# ============================================================================

class Medication(BaseModel):
    """Model for a single medication"""
    medication_id: str
    name: str
    dosage: str
    frequency: str  # e.g., "BID", "TID", "QD"
    scheduled_times: List[str]  # e.g., ["08:00", "20:00"]
    refill_days_remaining: Optional[int] = None
    instructions: Optional[str] = None


class PatientProfile(BaseModel):
    """Model for patient profile"""
    patient_id: str
    name: str
    age: int
    conditions: List[str]
    medications: List[Medication]
    phone: Optional[str] = None
    email: Optional[str] = None
    timezone: str = "America/New_York"
    preferences: Dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


# ============================================================================
# Adherence Log Models
# ============================================================================

class AdherenceLog(BaseModel):
    """Model for medication adherence log entry"""
    log_id: Optional[str] = None
    patient_id: str
    medication_id: str
    action: str  # "took", "skipped", "snoozed"
    reason: Optional[str] = None  # "timing_conflict", "supplement_interference", "side_effects", "other"
    notes: Optional[str] = None
    timestamp: str
    created_at: Optional[str] = None


# ============================================================================
# Intervention Models
# ============================================================================

class Intervention(BaseModel):
    """Model for agent intervention"""
    intervention_id: Optional[str] = None
    patient_id: str
    workflow_id: Optional[str] = None
    root_cause: str
    interventions: List[Dict[str, Any]]
    risk_assessment: Dict[str, Any]
    execution_results: List[Dict[str, Any]]
    expected_outcome: str
    timestamp: str
    created_at: Optional[str] = None


# ============================================================================
# Firestore Collection Names
# ============================================================================

class Collections:
    """Firestore collection names"""
    PATIENTS = "patients"
    ADHERENCE_LOGS = "adherence_logs"
    INTERVENTIONS = "interventions"
    WORKFLOWS = "workflows"
    AGENT_LOGS = "agent_logs"


# ============================================================================
# Sample Data Templates
# ============================================================================

def get_sample_patient() -> Dict[str, Any]:
    """Get a sample patient profile for testing"""
    return {
        "patient_id": "p001",
        "name": "John Smith",
        "age": 62,
        "conditions": ["Type 2 Diabetes", "Hypertension"],
        "medications": [
            {
                "medication_id": "med_001",
                "name": "Metformin",
                "dosage": "500 mg",
                "frequency": "BID",
                "scheduled_times": ["08:00", "20:00"],
                "refill_days_remaining": 18,
                "instructions": "Take with food"
            },
            {
                "medication_id": "med_002",
                "name": "Lisinopril",
                "dosage": "10 mg",
                "frequency": "QD",
                "scheduled_times": ["08:00"],
                "refill_days_remaining": 25,
                "instructions": "Take in the morning"
            }
        ],
        "phone": "+1-555-0123",
        "email": "john.smith@example.com",
        "timezone": "America/New_York",
        "preferences": {
            "notification_enabled": True,
            "reminder_sound": "gentle",
            "quiet_hours": {"start": "22:00", "end": "07:00"}
        },
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }


def get_sample_adherence_log() -> Dict[str, Any]:
    """Get a sample adherence log for testing"""
    return {
        "patient_id": "p001",
        "medication_id": "med_001",
        "action": "skipped",
        "reason": "forgot",
        "notes": "Rushed morning routine",
        "timestamp": datetime.utcnow().isoformat(),
        "created_at": datetime.utcnow().isoformat()
    }


def get_sample_intervention() -> Dict[str, Any]:
    """Get a sample intervention record for testing"""
    return {
        "patient_id": "p001",
        "workflow_id": "wf_20260217120000",
        "root_cause": "Behavioral pattern: Consistently forgets on Monday",
        "interventions": [
            {
                "type": "schedule_adjustment",
                "action": "Adjust reminder time for specific day",
                "details": {
                    "target_day": "Monday",
                    "adjustment": "30 minutes earlier",
                    "reason": "Account for different morning routine"
                }
            }
        ],
        "risk_assessment": {
            "approved": True,
            "risk_level": "low"
        },
        "execution_results": [
            {
                "intervention_type": "schedule_adjustment",
                "status": "success",
                "details": "Schedule adjusted for Monday: 30 minutes earlier"
            }
        ],
        "expected_outcome": "Reduce missed doses on Monday by 80%",
        "timestamp": datetime.utcnow().isoformat(),
        "created_at": datetime.utcnow().isoformat()
    }
