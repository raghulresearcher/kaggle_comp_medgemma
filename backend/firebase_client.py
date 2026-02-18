"""
Firebase Integration Module
Handles all Firebase Firestore operations for patient data management
"""
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore
from backend.config import config

logger = logging.getLogger(__name__)


class FirebaseClient:
    """
    Singleton Firebase client for Firestore operations
    """
    
    _instance = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize Firebase Admin SDK"""
        try:
            # Check if already initialized
            if not firebase_admin._apps:
                cred = credentials.Certificate(config.FIREBASE_CREDENTIALS_PATH)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': config.FIREBASE_DATABASE_URL
                })
                logger.info("Firebase Admin SDK initialized successfully")
            
            self._db = firestore.client()
            logger.info("Firestore client connected")
            
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {str(e)}")
            raise
    
    @property
    def db(self):
        """Get Firestore database instance"""
        return self._db


# ============================================================================
# Patient Operations
# ============================================================================

class PatientService:
    """Service for patient data operations"""
    
    def __init__(self):
        self.db = FirebaseClient().db
        self.collection = "patients"
    
    def get_patient(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """
        Get patient profile by ID
        
        Args:
            patient_id: Patient identifier
            
        Returns:
            Patient data dictionary or None if not found
        """
        try:
            doc = self.db.collection(self.collection).document(patient_id).get()
            
            if doc.exists:
                patient_data = doc.to_dict()
                patient_data['patient_id'] = patient_id
                logger.info(f"Retrieved patient: {patient_id}")
                return patient_data
            else:
                logger.warning(f"Patient not found: {patient_id}")
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving patient {patient_id}: {str(e)}")
            raise
    
    def create_patient(self, patient_data: Dict[str, Any]) -> str:
        """
        Create a new patient record
        
        Args:
            patient_data: Patient information dictionary
            
        Returns:
            Patient ID
        """
        try:
            patient_id = patient_data.get("patient_id")
            if not patient_id:
                raise ValueError("patient_id is required")
            
            # Add timestamps
            patient_data["created_at"] = firestore.SERVER_TIMESTAMP
            patient_data["updated_at"] = firestore.SERVER_TIMESTAMP
            
            self.db.collection(self.collection).document(patient_id).set(patient_data)
            logger.info(f"Created patient: {patient_id}")
            
            return patient_id
            
        except Exception as e:
            logger.error(f"Error creating patient: {str(e)}")
            raise
    
    def update_patient(self, patient_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update patient information
        
        Args:
            patient_id: Patient identifier
            updates: Dictionary of fields to update
            
        Returns:
            Success status
        """
        try:
            updates["updated_at"] = firestore.SERVER_TIMESTAMP
            
            self.db.collection(self.collection).document(patient_id).update(updates)
            logger.info(f"Updated patient: {patient_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating patient {patient_id}: {str(e)}")
            raise


# ============================================================================
# Adherence Log Operations
# ============================================================================

class AdherenceService:
    """Service for medication adherence logging"""
    
    def __init__(self):
        self.db = FirebaseClient().db
        self.collection = "adherence_logs"
    
    def log_action(self, action_data: Dict[str, Any]) -> str:
        """
        Log a medication action (took, skipped, snoozed)
        
        Args:
            action_data: Action information dictionary
            
        Returns:
            Log entry ID
        """
        try:
            # Add timestamp if not provided
            if "timestamp" not in action_data:
                action_data["timestamp"] = datetime.utcnow().isoformat()
            
            action_data["created_at"] = firestore.SERVER_TIMESTAMP
            
            doc_ref = self.db.collection(self.collection).add(action_data)
            log_id = doc_ref[1].id
            
            logger.info(f"Logged action for patient {action_data.get('patient_id')}: {action_data.get('action')}")
            
            return log_id
            
        except Exception as e:
            logger.error(f"Error logging action: {str(e)}")
            raise
    
    def get_patient_logs(
        self,
        patient_id: str,
        days: int = 30,
        action_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get adherence logs for a patient
        
        Args:
            patient_id: Patient identifier
            days: Number of days to retrieve (default 30)
            action_type: Filter by action type (took/skipped/snoozed)
            
        Returns:
            List of log entries
        """
        try:
            # Calculate date range
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Build query
            query = self.db.collection(self.collection) \
                .where(filter=firestore.FieldFilter("patient_id", "==", patient_id)) \
                .where(filter=firestore.FieldFilter("timestamp", ">=", start_date.isoformat())) \
                .order_by("timestamp", direction=firestore.Query.DESCENDING)
            
            if action_type:
                query = query.where(filter=firestore.FieldFilter("action", "==", action_type))
            
            # Execute query
            docs = query.stream()
            logs = []
            
            for doc in docs:
                log_data = doc.to_dict()
                log_data['log_id'] = doc.id
                logs.append(log_data)
            
            logger.info(f"Retrieved {len(logs)} logs for patient {patient_id}")
            return logs
            
        except Exception as e:
            logger.error(f"Error retrieving logs for patient {patient_id}: {str(e)}")
            raise
    
    def calculate_adherence_rate(
        self,
        patient_id: str,
        days: int = 7
    ) -> Dict[str, Any]:
        """
        Calculate adherence statistics for a patient
        
        Args:
            patient_id: Patient identifier
            days: Number of days to analyze
            
        Returns:
            Dictionary with adherence statistics
        """
        try:
            logs = self.get_patient_logs(patient_id, days=days)
            
            total_doses = len(logs)
            took_doses = len([log for log in logs if log.get("action") == "took"])
            skipped_doses = len([log for log in logs if log.get("action") == "skipped"])
            
            adherence_rate = (took_doses / total_doses * 100) if total_doses > 0 else 0.0
            
            return {
                "patient_id": patient_id,
                "period_days": days,
                "total_doses": total_doses,
                "took_doses": took_doses,
                "skipped_doses": skipped_doses,
                "adherence_rate": round(adherence_rate, 2),
                "calculated_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error calculating adherence for patient {patient_id}: {str(e)}")
            raise


# ============================================================================
# Intervention History Operations
# ============================================================================

class InterventionService:
    """Service for tracking agent interventions"""
    
    def __init__(self):
        self.db = FirebaseClient().db
        self.collection = "interventions"
    
    def log_intervention(self, intervention_data: Dict[str, Any]) -> str:
        """
        Log an agent intervention
        
        Args:
            intervention_data: Intervention details
            
        Returns:
            Intervention ID
        """
        try:
            intervention_data["created_at"] = firestore.SERVER_TIMESTAMP
            
            doc_ref = self.db.collection(self.collection).add(intervention_data)
            intervention_id = doc_ref[1].id
            
            logger.info(f"Logged intervention for patient {intervention_data.get('patient_id')}")
            
            return intervention_id
            
        except Exception as e:
            logger.error(f"Error logging intervention: {str(e)}")
            raise
    
    def get_patient_interventions(
        self,
        patient_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get recent interventions for a patient
        
        Args:
            patient_id: Patient identifier
            limit: Maximum number of interventions to return
            
        Returns:
            List of intervention records
        """
        try:
            docs = self.db.collection(self.collection) \
                .where(filter=firestore.FieldFilter("patient_id", "==", patient_id)) \
                .order_by("created_at", direction=firestore.Query.DESCENDING) \
                .limit(limit) \
                .stream()
            
            interventions = []
            for doc in docs:
                intervention_data = doc.to_dict()
                intervention_data['intervention_id'] = doc.id
                interventions.append(intervention_data)
            
            logger.info(f"Retrieved {len(interventions)} interventions for patient {patient_id}")
            return interventions
            
        except Exception as e:
            logger.error(f"Error retrieving interventions for patient {patient_id}: {str(e)}")
            raise


# ============================================================================
# Convenience Functions
# ============================================================================

# Global service instances
patient_service = PatientService()
adherence_service = AdherenceService()
intervention_service = InterventionService()


def get_patient(patient_id: str) -> Optional[Dict[str, Any]]:
    """Convenience function to get patient"""
    return patient_service.get_patient(patient_id)


def log_medication_action(action_data: Dict[str, Any]) -> str:
    """Convenience function to log medication action"""
    return adherence_service.log_action(action_data)


def get_adherence_summary(patient_id: str, days: int = 7) -> Dict[str, Any]:
    """Convenience function to get adherence summary"""
    return adherence_service.calculate_adherence_rate(patient_id, days)


if __name__ == "__main__":
    # Test Firebase connection (requires credentials to be configured)
    print("Testing Firebase connection...")
    try:
        client = FirebaseClient()
        print("Firebase connected successfully!")
    except Exception as e:
        print(f"Firebase connection failed: {str(e)}")
