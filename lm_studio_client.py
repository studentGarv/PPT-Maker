import requests
import json
import re
from typing import List, Dict, Optional
from config import DEFAULT_SLIDES_COUNT, AI_PROVIDERS


class LMStudioClient:
    """Client for interacting with LM Studio local server (OpenAI-compatible API)"""
    
    def __init__(self, base_url: str = "http://localhost:1234", model: str = None):
        self.base_url = base_url.rstrip('/')
        # Use provided model or default from config
        self.model = model or AI_PROVIDERS["lm_studio"]["default_model"]
        self.api_url = f"{self.base_url}/v1"
        self._best_model = None  # Cache for best model selection
        
        # Timeout settings from config
        self.timeouts = AI_PROVIDERS["lm_studio"].get("timeout", {
            "connection": 10,
            "outline": 300,
            "enhancement": 120
        })
        
    def get_model_to_use(self) -> str:
        """Get the model to use for API calls"""
        if self.model:
            return self.model  # Use explicitly specified model
        
        if not self._best_model:
            self._best_model = self.select_best_model()
        
        return self._best_model
        
    def _make_request(self, endpoint: str, data: dict, timeout: int = 180) -> dict:
        """Make a request to the LM Studio API with configurable timeout"""
        url = f"{self.api_url}/{endpoint}"
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            print(f"🔄 Making request to LM Studio (timeout: {timeout}s)...")
            response = requests.post(url, json=data, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout as e:
            raise Exception(f"LM Studio request timed out after {timeout}s. Try reducing slide count or using a faster model.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"LM Studio API error: {e}")
    
    def test_connection(self) -> bool:
        """Test connection to LM Studio server"""
        try:
            # Try to get available models
            response = requests.get(f"{self.api_url}/models", timeout=self.timeouts["connection"])
            return response.status_code == 200
        except:
            return False
    
    def get_available_models(self) -> List[str]:
        """Get list of available models from LM Studio"""
        try:
            response = requests.get(f"{self.api_url}/models", timeout=self.timeouts["connection"])
            if response.status_code == 200:
                models_data = response.json()
                return [model["id"] for model in models_data.get("data", [])]
            return []
        except:
            return []
    
    def get_loaded_model(self) -> str:
        """Get the currently loaded/active model in LM Studio"""
        try:
            # Try to get model info from a simple completion request
            data = {
                "model": "local-model",
                "messages": [{"role": "user", "content": "test"}],
                "max_tokens": 1,
                "temperature": 0
            }
            
            response = requests.post(f"{self.api_url}/chat/completions", 
                                   json=data, timeout=5)
            if response.status_code == 200:
                result = response.json()
                return result.get("model", "local-model")
            else:
                # If API call fails, try to infer from available models
                models = self.get_available_models()
                if models:
                    # Prefer chat/instruct models for presentation generation
                    chat_models = [m for m in models if any(keyword in m.lower() 
                                                          for keyword in ['instruct', 'chat', 'llama', 'mistral'])]
                    return chat_models[0] if chat_models else models[0]
                return "local-model"
        except:
            return "local-model"
    
    def select_best_model(self) -> str:
        """Select the best available model for presentation generation"""
        models = self.get_available_models()
        
        if not models:
            return "local-model"
        
        # Priority order for presentation generation (GPT OSS 20B first)
        preferred_keywords = [
            'gpt-oss-20b',     # GPT OSS 20B - highest priority
            'gpt-oss',         # Other GPT OSS models
            'gpt',             # GPT-style models
            'llama',           # Llama models are generally good for text generation
            'instruct',        # Instruction-tuned models
            'chat',            # Chat models work well for structured output
            'mistral',         # Mistral models are good for creative tasks
            'qwen'             # Qwen models are capable
        ]
        
        # Filter out embedding models (not suitable for text generation)
        text_models = [m for m in models if 'embedding' not in m.lower()]
        
        if not text_models:
            return models[0]  # Fallback to first available
        
        # Find best match based on preferred keywords
        for keyword in preferred_keywords:
            for model in text_models:
                if keyword in model.lower():
                    return model
        
        # If no preferred model found, return first text model
        return text_models[0]
    
    def generate_presentation_outline(self, prompt: str, num_slides: int = DEFAULT_SLIDES_COUNT) -> Dict:
        """Generate a presentation outline based on the prompt"""
        
        system_prompt = f"""You are an expert presentation designer. Create a detailed outline for a PowerPoint presentation based on the user's request.

Return your response as a JSON object with the following structure:
{{
    "title": "Main presentation title",
    "slides": [
        {{
            "slide_number": 1,
            "title": "Slide title",
            "content": [
                "Bullet point 1",
                "Bullet point 2",
                "Bullet point 3"
            ]
        }}
    ]
}}

Guidelines:
- Create exactly {num_slides} slides (including title slide)
- Keep titles concise and engaging
- Use 3-5 bullet points per slide for content slides
- Make content informative and well-structured
- Ensure logical flow between slides
- The first slide should be the title slide with presentation title and subtitle/overview
- The last slide should be a conclusion with a impactful statement or key message
- Avoid repetitive content across slides"""

        user_prompt = f"Create a presentation about: {prompt}"
        
        try:
            model_to_use = self.get_model_to_use()
            data = {
                "model": model_to_use,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            print(f"🤖 Using LM Studio model: {model_to_use}")
            print(f"⏱️ Generating outline for {num_slides} slides (this may take up to {self.timeouts['outline']//60} minutes for large models)...")
            
            # Use configured timeout for outline generation
            response = self._make_request("chat/completions", data, timeout=self.timeouts["outline"])
            
            # Extract content from response
            content = response["choices"][0]["message"]["content"]
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                # Fallback if JSON parsing fails
                return self._create_fallback_outline(prompt, num_slides)
                
        except Exception as e:
            print(f"Error generating outline with LM Studio: {e}")
            return self._create_fallback_outline(prompt, num_slides)
    
    def enhance_slide_content(self, title: str, basic_content: List[str]) -> List[str]:
        """Enhance slide content with more detailed information"""
        
        prompt = f"""Enhance the following slide content for a presentation slide titled "{title}".
        
Current content:
{chr(10).join(f"- {item}" for item in basic_content)}

Please provide enhanced, more detailed bullet points that are:
- More specific and informative
- Professional and engaging
- Properly formatted
- Limited to 3-5 points

IMPORTANT: Return ONLY the enhanced bullet points, one per line, without bullet symbols. Do not include any introductory text, explanations, or phrases like "Here is..." or "Enhanced version:". Start directly with the first bullet point."""

        try:
            model_to_use = self.get_model_to_use()
            data = {
                "model": model_to_use,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            response = self._make_request("chat/completions", data, timeout=self.timeouts["enhancement"])  # Use configured timeout for content enhancement
            content = response["choices"][0]["message"]["content"]
            
            # Filter out any introductory text or unwanted phrases
            lines = content.split('\n')
            enhanced_points = []
            
            for line in lines:
                line = line.strip()
                if line and not any(phrase in line.lower() for phrase in [
                    'here is', 'enhanced version', 'here are', 'improved content',
                    'better version', 'updated content', 'enhanced bullet points'
                ]):
                    # Remove any bullet symbols or numbering
                    line = re.sub(r'^[-•*\d+\.)\s]+', '', line).strip()
                    if line:
                        enhanced_points.append(line)
            
            return enhanced_points[:5] if enhanced_points else basic_content  # Limit to 5 points
            
        except Exception as e:
            print(f"Error enhancing content with LM Studio: {e}")
            return basic_content
    
    def _create_fallback_outline(self, prompt: str, num_slides: int) -> Dict:
        """Create a basic outline if AI generation fails"""
        
        # Create a more dynamic fallback based on the number of slides
        slides = []
        
        # Title slide
        slides.append({
            "slide_number": 1,
            "title": prompt,
            "content": ["Overview", "Key Topics", "Objectives"]
        })
        
        # Content slides
        if num_slides >= 3:
            slides.append({
                "slide_number": 2,
                "title": "Introduction",
                "content": ["Background", "Context", "Importance", "Scope"]
            })
        
        if num_slides >= 4:
            slides.append({
                "slide_number": 3,
                "title": "Main Content",
                "content": ["Key Point 1", "Key Point 2", "Key Point 3", "Supporting Details"]
            })
        
        # Add more content slides if needed
        for i in range(4, num_slides):
            slides.append({
                "slide_number": i,
                "title": f"Additional Topic {i-2}",
                "content": [f"Point {j}" for j in range(1, 5)]
            })
        
        # Conclusion slide (always last)
        if num_slides >= 2:
            slides.append({
                "slide_number": num_slides,
                "title": "Thank You",
                "content": ["Thank you for your attention!"]
            })
        
        return {
            "title": f"Presentation: {prompt}",
            "slides": slides[:num_slides]
        }
