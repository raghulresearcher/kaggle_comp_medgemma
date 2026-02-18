"""
MedGemma HF Integration - LangChain Wrapper
Provides interface to MedGemma model via Hugging Face Inference Endpoint
"""
import logging
import requests
from typing import Any, Dict, List, Optional
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from pydantic import Field

logger = logging.getLogger(__name__)


class MedGemmaHF(LLM):
    """
    LangChain-compatible wrapper for MedGemma via Hugging Face Inference Endpoint
    
    Endpoint: https://xtwm07qt8ypxfwon.us-east-1.aws.endpoints.huggingface.cloud
    """
    
    endpoint_url: str = Field(default="https://xtwm07qt8ypxfwon.us-east-1.aws.endpoints.huggingface.cloud")
    api_key: str = Field(default="")
    timeout: int = Field(default=120)
    temperature: float = Field(default=0.7)
    max_tokens: int = Field(default=512)
    
    @property
    def _llm_type(self) -> str:
        """Return identifier for this LLM"""
        return "medgemma_hf"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """
        Call the MedGemma VM inference endpoint
        
        Args:
            prompt: The input prompt for medical reasoning
            stop: List of stop sequences (optional)
            run_manager: Callback manager (optional)
            **kwargs: Additional parameters
            
        Returns:
            The model's response text
        """
        try:
            logger.info(f"Calling MedGemma HF endpoint")
            logger.debug(f"Prompt: {prompt[:100]}...")
            
            # Prepare request payload for HF Inference Endpoint
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": kwargs.get("max_tokens", self.max_tokens),
                    "temperature": kwargs.get("temperature", self.temperature)
                }
            }
            
            # Make HTTP request to HF endpoint
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                self.endpoint_url,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            # Parse response (HF returns [{"input_text": "...", "generated_text": "..."}])
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get("generated_text", "")
            else:
                generated_text = ""
            
            logger.info(f"MedGemma response received ({len(generated_text)} chars)")
            logger.debug(f"Response: {generated_text[:100]}...")
            
            return generated_text
            
        except requests.exceptions.Timeout:
            logger.error(f"MedGemma HF request timed out after {self.timeout}s")
            raise TimeoutError(f"MedGemma HF request timed out after {self.timeout}s")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"MedGemma HF request failed: {str(e)}")
            raise ConnectionError(f"Failed to connect to MedGemma HF endpoint: {str(e)}")
            
        except Exception as e:
            logger.error(f"Unexpected error calling MedGemma HF: {str(e)}")
            raise
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check if the MedGemma HF endpoint is healthy and responsive
        
        Returns:
            Dictionary with health status information
        """
        try:
            # Simple test call to verify endpoint is working
            test_response = self._call("Test prompt", max_tokens=10)
            
            return {
                "status": "healthy",
                "endpoint_url": self.endpoint_url,
                "response": "Endpoint responding normally"
            }
            
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "endpoint_url": self.endpoint_url,
                "error": str(e)
            }
    
    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return identifying parameters for this LLM"""
        return {
            "endpoint_url": self.endpoint_url,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "timeout": self.timeout
        }


# ============================================================================
# Utility Functions
# ============================================================================

def create_medical_prompt(
    question: str,
    context: Optional[str] = None,
    format_instructions: Optional[str] = None
) -> str:
    """
    Create a well-formatted prompt for MedGemma
    
    Args:
        question: The medical question or task
        context: Additional context (patient info, medications, etc.)
        format_instructions: How to format the response
        
    Returns:
        Formatted prompt string
    """
    prompt_parts = []
    
    # System instruction
    prompt_parts.append(
        "You are a medical AI assistant specializing in medication adherence. "
        "Provide accurate, evidence-based guidance. Always prioritize patient safety."
    )
    
    # Context if provided
    if context:
        prompt_parts.append(f"\n\nContext:\n{context}")
    
    # Main question
    prompt_parts.append(f"\n\nQuestion:\n{question}")
    
    # Format instructions if provided
    if format_instructions:
        prompt_parts.append(f"\n\nPlease respond in the following format:\n{format_instructions}")
    
    return "\n".join(prompt_parts)


def validate_drug_interaction(
    medication1: str,
    medication2: str,
    llm: MedGemmaHF
) -> Dict[str, Any]:
    """
    Use MedGemma HF to check for drug interactions
    
    Args:
        medication1: First medication name
        medication2: Second medication name (or substance like food, alcohol)
        llm: MedGemma HF instance
        
    Returns:
        Dictionary with interaction information
    """
    prompt = create_medical_prompt(
        question=f"Are there any interactions between {medication1} and {medication2}?",
        format_instructions=(
            "Respond with:\n"
            "- Interaction Level: None/Minor/Moderate/Severe\n"
            "- Description: Brief explanation\n"
            "- Recommendation: What the patient should do"
        )
    )
    
    try:
        response = llm.invoke(prompt)
        
        # Parse response (basic parsing - can be enhanced)
        return {
            "medication1": medication1,
            "medication2": medication2,
            "response": response,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Drug interaction check failed: {str(e)}")
        return {
            "medication1": medication1,
            "medication2": medication2,
            "error": str(e),
            "status": "error"
        }


def assess_side_effect(
    medication: str,
    symptom: str,
    severity: str,
    llm: MedGemmaHF
) -> Dict[str, Any]:
    """
    Use MedGemma HF to assess if a symptom is a known side effect
    
    Args:
        medication: Medication name
        symptom: Reported symptom
        severity: Symptom severity (mild/moderate/severe)
        llm: MedGemma HF instance
        
    Returns:
        Dictionary with assessment information
    """
    prompt = create_medical_prompt(
        question=(
            f"Patient reports {symptom} (severity: {severity}) after taking {medication}. "
            f"Is this a known side effect? Should the patient seek immediate medical attention?"
        ),
        format_instructions=(
            "Respond with:\n"
            "- Is Known Side Effect: Yes/No\n"
            "- Urgency: Emergency/See Doctor Soon/Can Manage at Home\n"
            "- Recommendations: What the patient should do\n"
            "- Warning Signs: When to seek immediate help"
        )
    )
    
    try:
        response = llm.invoke(prompt)
        
        return {
            "medication": medication,
            "symptom": symptom,
            "severity": severity,
            "response": response,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Side effect assessment failed: {str(e)}")
        return {
            "medication": medication,
            "symptom": symptom,
            "error": str(e),
            "status": "error"
        }


if __name__ == "__main__":
    # Test the MedGemma HF endpoint connection
    print("Testing MedGemma HF endpoint connection...")
    
    llm = MedGemmaHF()
    
    # Health check
    health = llm.health_check()
    print(f"Health check: {health}")
    
    # Test inference (uncomment to test)
    # response = llm.invoke("What is Metformin used for?")
    # print(f"Response: {response}")
