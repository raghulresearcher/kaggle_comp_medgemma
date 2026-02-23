"""
Unit tests for MedGemma HF wrapper
"""
import pytest
from unittest.mock import Mock, patch
from backend.agents.medgemma_hf import MedGemmaHF


class TestMedGemmaHF:
    """Test cases for MedGemma Hugging Face wrapper"""
    
    def test_initialization(self):
        """Test that MedGemma wrapper initializes correctly"""
        llm = MedGemmaHF()
        assert llm is not None
        assert llm.max_tokens == 512
        assert llm.temperature == 0.7
    
    def test_initialization_with_custom_params(self):
        """Test initialization with custom parameters"""
        llm = MedGemmaHF(max_tokens=1024, temperature=0.5)
        assert llm.max_tokens == 1024
        assert llm.temperature == 0.5
    
    @patch('backend.agents.medgemma_hf.requests.post')
    def test_text_only_call(self, mock_post):
        """Test text-only API call"""
        mock_response = Mock()
        mock_response.json.return_value = [{
            "generated_text": "This is a medical response."
        }]
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        llm = MedGemmaHF()
        result = llm.invoke("What is hypertension?")
        
        assert "This is a medical response" in result
        mock_post.assert_called_once()
    
    @patch('backend.agents.medgemma_hf.requests.post')
    def test_vision_call_with_image(self, mock_post):
        """Test multimodal API call with image"""
        mock_response = Mock()
        mock_response.json.return_value = [{
            "generated_text": "Rash analysis: Mild urticarial reaction."
        }]
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        llm = MedGemmaHF()
        result = llm.invoke(
            "Analyze this rash",
            image="data:image/jpeg;base64,test_image_data"
        )
        
        assert "Rash analysis" in result
        # Verify image was sent in payload
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        assert 'inputs' in payload
        assert 'image' in payload['inputs']
    
    @patch('backend.agents.medgemma_hf.requests.post')
    def test_temporal_tracking_with_previous_images(self, mock_post):
        """Test temporal tracking with previous images array"""
        mock_response = Mock()
        mock_response.json.return_value = [{
            "generated_text": "Comparing Day 3→4→5: Healing progression detected."
        }]
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        llm = MedGemmaHF()
        result = llm.invoke(
            "Compare healing progression",
            image="data:image/jpeg;base64,day5_image",
            previous_images=[
                "data:image/jpeg;base64,day3_image",
                "data:image/jpeg;base64,day4_image"
            ]
        )
        
        assert "Healing progression" in result
    
    @patch('backend.agents.medgemma_hf.requests.post')
    def test_api_error_handling(self, mock_post):
        """Test handling of API errors"""
        mock_post.side_effect = Exception("API connection failed")
        
        llm = MedGemmaHF()
        
        with pytest.raises(Exception):
            llm.invoke("Test prompt")
    
    def test_llm_type_property(self):
        """Test that _llm_type property returns correct value"""
        llm = MedGemmaHF()
        assert llm._llm_type == "medgemma_hf"
