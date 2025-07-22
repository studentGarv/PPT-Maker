#!/usr/bin/env python3
"""
PPT Maker Web Interface
A web-based interface for generating PowerPoint presentations
"""

import gradio as gr
import os
import tempfile
from ppt_generator import PPTGenerator
import traceback


class PPTMakerWeb:
    def __init__(self):
        self.generator = PPTGenerator()
    
    def generate_presentation_web(self, prompt, num_slides, model_name, enhance_content):
        """Generate presentation through web interface"""
        try:
            if not prompt.strip():
                return None, "❌ Please enter a presentation topic"
            
            if num_slides < 2 or num_slides > 20:
                return None, "❌ Number of slides must be between 2 and 20"
            
            # Test Ollama connection
            if not self.generator.test_ollama_connection():
                return None, "❌ Cannot connect to Ollama. Please make sure Ollama is running with: ollama serve"
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.pptx', delete=False) as tmp_file:
                output_path = tmp_file.name
            
            # Update model if different
            if model_name != self.generator.ollama_client.model:
                self.generator.ollama_client.model = model_name
            
            # Generate presentation
            success = self.generator.generate_presentation(
                prompt=prompt,
                output_file=output_path,
                num_slides=num_slides,
                enhance_content=enhance_content
            )
            
            if success:
                return output_path, f"✅ Presentation created successfully! ({num_slides} slides)"
            else:
                return None, "❌ Failed to generate presentation"
                
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            print(f"Full error: {traceback.format_exc()}")
            return None, error_msg
    
    def get_available_models(self):
        """Get list of available Ollama models"""
        try:
            models = self.generator.list_available_models()
            return models if models else ["llama3"]
        except:
            return ["llama3", "mistral", "llama2"]
    
    def create_interface(self):
        """Create Gradio web interface"""
        
        # Get available models
        available_models = self.get_available_models()
        
        with gr.Blocks(title="PPT Maker", theme=gr.themes.Soft()) as interface:
            gr.Markdown("# 🎯 PPT Maker")
            gr.Markdown("Generate professional PowerPoint presentations from text prompts using AI")
            
            with gr.Row():
                with gr.Column(scale=2):
                    prompt_input = gr.Textbox(
                        label="Presentation Topic",
                        placeholder="Enter your presentation topic (e.g., 'Artificial Intelligence in Healthcare')",
                        lines=3
                    )
                    
                    with gr.Row():
                        slides_input = gr.Slider(
                            minimum=2,
                            maximum=20,
                            value=8,
                            step=1,
                            label="Number of Slides"
                        )
                        
                        model_input = gr.Dropdown(
                            choices=available_models,
                            value=available_models[0],
                            label="AI Model"
                        )
                    
                    enhance_input = gr.Checkbox(
                        value=True,
                        label="Enhance Content (more detailed but slower)"
                    )
                    
                    generate_btn = gr.Button("🚀 Generate Presentation", variant="primary", size="lg")
                
                with gr.Column(scale=1):
                    status_output = gr.Textbox(
                        label="Status",
                        interactive=False,
                        lines=3
                    )
                    
                    download_output = gr.File(
                        label="Download Presentation",
                        interactive=False
                    )
            
            # Examples
            gr.Markdown("## 💡 Example Topics")
            gr.Examples(
                examples=[
                    ["Introduction to Machine Learning", 10, "llama3", True],
                    ["Business Plan for Tech Startup", 12, "llama3", True],
                    ["Climate Change Solutions", 8, "llama3", False],
                    ["Python Programming Basics", 15, "llama3", True],
                    ["Digital Marketing Strategies", 9, "llama3", True]
                ],
                inputs=[prompt_input, slides_input, model_input, enhance_input]
            )
            
            # Setup event handler
            generate_btn.click(
                fn=self.generate_presentation_web,
                inputs=[prompt_input, slides_input, model_input, enhance_input],
                outputs=[download_output, status_output]
            )
        
        return interface


def main():
    """Launch the web application"""
    print("🚀 Starting PPT Maker Web Interface...")
    
    # Create web app
    app = PPTMakerWeb()
    interface = app.create_interface()
    
    # Launch with public access
    interface.launch(
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,
        share=True,  # Create public link
        show_error=True
    )


if __name__ == "__main__":
    main()
