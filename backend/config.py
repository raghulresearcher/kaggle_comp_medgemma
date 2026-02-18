"""
Configuration management for MedAdhere Pro backend
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from project root
project_root = Path(__file__).parent.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Application configuration"""
    
    # Flask settings
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Server settings
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    
    # GCP settings
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "")
    GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1")
    
    # MedGemma settings (Hugging Face Inference Endpoint)
    MEDGEMMA_ENDPOINT = os.getenv("MEDGEMMA_ENDPOINT", "https://xtwm07qt8ypxfwon.us-east-1.aws.endpoints.huggingface.cloud")
    MEDGEMMA_API_KEY = os.getenv("HF_API_KEY", "")
    MEDGEMMA_TIMEOUT = int(os.getenv("MEDGEMMA_TIMEOUT", "120"))
    MEDGEMMA_TEMPERATURE = float(os.getenv("MEDGEMMA_TEMPERATURE", "0.7"))
    MEDGEMMA_MAX_TOKENS = int(os.getenv("MEDGEMMA_MAX_TOKENS", "512"))
    
    # Firebase settings
    FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH", "")
    FIREBASE_DATABASE_URL = os.getenv("FIREBASE_DATABASE_URL", "")
    
    # Agent settings
    AGENT_MAX_ITERATIONS = int(os.getenv("AGENT_MAX_ITERATIONS", "5"))
    AGENT_TIMEOUT = int(os.getenv("AGENT_TIMEOUT", "300"))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/medadhere.log")
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required = ["GCP_PROJECT_ID", "FIREBASE_CREDENTIALS_PATH"]
        missing = [key for key in required if not getattr(cls, key)]
        
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
        
        return True


# Singleton config instance
config = Config()
