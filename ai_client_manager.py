from typing import List, Dict, Optional, Union
from ollama_client import OllamaClient
from lm_studio_client import LMStudioClient
from config import DEFAULT_MODEL, DEFAULT_SLIDES_COUNT


class AIClientManager:
    """Manager for different AI clients (Ollama, LM Studio, etc.)"""
    
    PROVIDER_OLLAMA = "ollama"
    PROVIDER_LM_STUDIO = "lm_studio"
    
    def __init__(self, provider: str = PROVIDER_OLLAMA, **kwargs):
        self.provider = provider
        self.client = None
        self._initialize_client(**kwargs)
    
    def _initialize_client(self, **kwargs):
        """Initialize the appropriate AI client based on provider"""
        if self.provider == self.PROVIDER_OLLAMA:
            base_url = kwargs.get('base_url', 'http://localhost:11434')
            model = kwargs.get('model', DEFAULT_MODEL)
            self.client = OllamaClient(base_url=base_url, model=model)
            
        elif self.provider == self.PROVIDER_LM_STUDIO:
            base_url = kwargs.get('base_url', 'http://localhost:1234')
            model = kwargs.get('model', None)  # LM Studio uses loaded model
            self.client = LMStudioClient(base_url=base_url, model=model)
            
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")
    
    def test_connection(self) -> bool:
        """Test connection to the AI service"""
        try:
            if hasattr(self.client, 'test_connection'):
                return self.client.test_connection()
            else:
                # For Ollama, try a simple generation
                result = self.client.generate_presentation_outline("test", 1)
                return result is not None
        except:
            return False
    
    def get_available_models(self) -> List[str]:
        """Get available models from the AI service"""
        if hasattr(self.client, 'get_available_models'):
            return self.client.get_available_models()
        else:
            return [DEFAULT_MODEL]  # Fallback for Ollama
    
    def generate_presentation_outline(self, prompt: str, num_slides: int = DEFAULT_SLIDES_COUNT) -> Dict:
        """Generate presentation outline using the configured AI client"""
        return self.client.generate_presentation_outline(prompt, num_slides)
    
    def enhance_slide_content(self, title: str, basic_content: List[str]) -> List[str]:
        """Enhance slide content using the configured AI client"""
        return self.client.enhance_slide_content(title, basic_content)
    
    @classmethod
    def create_client(cls, provider: str, **kwargs) -> 'AIClientManager':
        """Factory method to create AI client manager"""
        return cls(provider=provider, **kwargs)
    
    @classmethod
    def auto_detect_provider(cls, **kwargs) -> 'AIClientManager':
        """Auto-detect and create the best available AI provider"""
        
        # Try LM Studio first
        try:
            lm_client = cls.create_client(cls.PROVIDER_LM_STUDIO, **kwargs)
            if lm_client.test_connection():
                print("✅ LM Studio detected and connected")
                return lm_client
        except Exception as e:
            print(f"❌ LM Studio not available: {e}")
        
        # Fallback to Ollama
        try:
            ollama_client = cls.create_client(cls.PROVIDER_OLLAMA, **kwargs)
            if ollama_client.test_connection():
                print("✅ Ollama detected and connected")
                return ollama_client
        except Exception as e:
            print(f"❌ Ollama not available: {e}")
        
        # If neither works, return Ollama as default (will show appropriate error)
        print("⚠️ No AI provider detected, defaulting to Ollama")
        return cls.create_client(cls.PROVIDER_OLLAMA, **kwargs)


def get_client_info(client_manager: AIClientManager) -> Dict[str, any]:
    """Get information about the current AI client"""
    return {
        "provider": client_manager.provider,
        "connected": client_manager.test_connection(),
        "available_models": client_manager.get_available_models()
    }
