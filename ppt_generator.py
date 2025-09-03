from ai_client_manager import AIClientManager
from pptx_generator import PPTXGenerator
from config import DEFAULT_SLIDES_COUNT, DEFAULT_OUTPUT_FILE, MAX_SLIDES_COUNT, MIN_SLIDES_COUNT, DEFAULT_MODEL, DEFAULT_AI_PROVIDER
from typing import Optional
import os


class PPTGenerator:
    """Main class for generating PowerPoint presentations from text prompts"""
    
    def __init__(self, model: str = None, ai_provider: str = None, base_url: str = None):
        """
        Initialize PPT Generator with configurable AI provider
        
        Args:
            model (str): Model name to use
            ai_provider (str): AI provider ('ollama' or 'lm_studio')
            base_url (str): Base URL for the AI service
        """
        # Use provided provider or default
        provider = ai_provider or DEFAULT_AI_PROVIDER
        
        # Prepare client configuration
        client_config = {}
        if base_url:
            client_config['base_url'] = base_url
        if model:
            client_config['model'] = model
        
        # Initialize AI client manager
        try:
            self.ai_client = AIClientManager.create_client(provider, **client_config)
        except Exception as e:
            print(f"⚠️ Error with {provider}, trying auto-detection: {e}")
            self.ai_client = AIClientManager.auto_detect_provider(**client_config)
        
        self.pptx_generator = PPTXGenerator()
    
    def generate_presentation(
        self, 
        prompt: str, 
        output_file: str = DEFAULT_OUTPUT_FILE,
        num_slides: int = DEFAULT_SLIDES_COUNT,
        enhance_content: bool = True
    ) -> bool:
        """
        Generate a PowerPoint presentation from a text prompt
        
        Args:
            prompt (str): The text prompt describing the presentation
            output_file (str): Output filename for the presentation
            num_slides (int): Number of slides to generate
            enhance_content (bool): Whether to enhance content using AI
            
        Returns:
            bool: True if successful, False otherwise
        """
        
        try:
            # Validate input
            if not prompt.strip():
                raise ValueError("Prompt cannot be empty")
            
            if num_slides < MIN_SLIDES_COUNT or num_slides > MAX_SLIDES_COUNT:
                raise ValueError(f"Number of slides must be between {MIN_SLIDES_COUNT} and {MAX_SLIDES_COUNT}")
            
            print(f"Generating presentation outline for: '{prompt}'...")
            
            # Generate presentation outline using AI client
            outline = self.ai_client.generate_presentation_outline(prompt, num_slides)
            
            if not outline or 'slides' not in outline:
                raise ValueError("Failed to generate presentation outline")
            
            print(f"Generated outline with {len(outline['slides'])} slides")
            
            # Create presentation
            presentation_title = outline.get('title', prompt)
            self.pptx_generator.create_presentation(presentation_title)
            
            # Add title slide
            self.pptx_generator.add_title_slide(
                title=presentation_title,
                subtitle="Generated with AI"
            )
            
            print("Creating slides...")
            
            # Add content slides
            for i, slide_data in enumerate(outline['slides']):
                slide_title = slide_data.get('title', f'Slide {i+1}')
                slide_content = slide_data.get('content', [])
                
                # Enhance content if requested
                if enhance_content and slide_content:
                    print(f"Enhancing content for slide: '{slide_title}'")
                    enhanced_content = self.ai_client.enhance_slide_content(
                        slide_title, 
                        slide_content
                    )
                    slide_content = enhanced_content
                
                # Determine slide type based on position and content
                if i == 0 and len(outline['slides']) > 1:
                    # First slide after title - make it an overview
                    self.pptx_generator.add_content_slide(slide_title, slide_content)
                elif i == len(outline['slides']) - 1 and len(outline['slides']) > 2:
                    # Last slide - conclusion
                    conclusion_keywords = ['conclusion', 'summary', 'takeaway', 'final', 'closing', 'end', 'thank']
                    if any(keyword in slide_title.lower() for keyword in conclusion_keywords):
                        # For conclusion slides, use only the first content item or create a summary
                        conclusion_content = [slide_content[0]] if slide_content else ["Thank you for your attention!"]
                        self.pptx_generator.add_conclusion_slide(slide_title, conclusion_content)
                    else:
                        # Even if not explicitly named as conclusion, treat last slide as conclusion
                        conclusion_content = [slide_content[0]] if slide_content else ["Thank you for your attention!"]
                        self.pptx_generator.add_conclusion_slide("Thank You", conclusion_content)
                else:
                    # Regular content slide
                    self.pptx_generator.add_content_slide(slide_title, slide_content)
                
                print(f"Added slide {i+1}: {slide_title}")
            
            # Check if we already added a proper conclusion slide
            last_slide_title = outline['slides'][-1].get('title', '').lower()
            conclusion_keywords = ['conclusion', 'summary', 'takeaway', 'final', 'closing', 'end', 'thank']
            has_conclusion = any(keyword in last_slide_title for keyword in conclusion_keywords)
            
            # Only add thank you slide if we don't have a conclusion and have more than 2 slides
            if not has_conclusion and len(outline['slides']) > 2:
                self.pptx_generator.add_conclusion_slide()
                print("Added thank you slide")
            
            # Save presentation
            print(f"Saving presentation to: {output_file}")
            success = self.pptx_generator.save_presentation(output_file)
            
            if success:
                print(f"✅ Presentation successfully created: {output_file}")
                return True
            else:
                print("❌ Failed to save presentation")
                return False
                
        except Exception as e:
            print(f"❌ Error generating presentation: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Test if AI service is accessible"""
        try:
            return self.ai_client.test_connection()
        except Exception as e:
            print(f"AI service connection test failed: {e}")
            return False
    
    def list_available_models(self) -> list:
        """List available models from AI service"""
        try:
            return self.ai_client.get_available_models()
        except Exception as e:
            print(f"Error listing models: {e}")
            return []


def main():
    """Example usage of the PPTGenerator"""
    
    generator = PPTGenerator()
    
    # Test AI service connection
    if not generator.test_connection():
        print("❌ Cannot connect to AI service. Please make sure your AI service is running.")
        print("For Ollama: ollama serve")
        print("For LM Studio: Start LM Studio and load a model")
        return
    
    print("✅ Connected to AI service successfully!")
    
    # List available models
    models = generator.list_available_models()
    if models:
        print(f"Available models: {', '.join(models)}")
    
    # Generate a test presentation
    test_prompt = "Artificial Intelligence and Machine Learning: Fundamentals and Applications"
    output_file = "ai_ml_presentation.pptx"
    
    success = generator.generate_presentation(
        prompt=test_prompt,
        output_file=output_file,
        num_slides=6,
        enhance_content=True
    )
    
    if success:
        print(f"\n🎉 Test presentation created successfully!")
        print(f"File: {os.path.abspath(output_file)}")
    else:
        print("\n❌ Failed to create test presentation")


if __name__ == "__main__":
    main()
