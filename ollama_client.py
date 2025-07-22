import ollama
import json
import re
from typing import List, Dict, Optional
from config import OLLAMA_BASE_URL, DEFAULT_MODEL, DEFAULT_SLIDES_COUNT


class OllamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = DEFAULT_MODEL):
        self.base_url = base_url
        self.model = model
        self.client = ollama.Client(host=base_url)
    
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
            response = self.client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            # Extract JSON from response
            content = response['message']['content']
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                # Fallback if JSON parsing fails
                return self._create_fallback_outline(prompt, num_slides)
                
        except Exception as e:
            print(f"Error generating outline: {e}")
            return self._create_fallback_outline(prompt, num_slides)
    
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
            response = self.client.chat(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response['message']['content']
            
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
            print(f"Error enhancing content: {e}")
            return basic_content
