import gradio as gr
import os
import tempfile
from ppt_generator import PPTGenerator
from rag_processor import RAGProcessor
from ppt_improver import improve_ppt
import traceback

class PPTMakerWeb:
    def __init__(self):
        self.generator = PPTGenerator()
        self.rag_processor = RAGProcessor()
    
    def generate_presentation_web(self, prompt, num_slides, model_name, enhance_content, uploaded_files, urls_text, use_rag):
        """Generate presentation through web interface"""
        try:
            if not prompt.strip():
                return None, "❌ Please enter a presentation topic"
            
            if num_slides < 2 or num_slides > 20:
                return None, "❌ Number of slides must be between 2 and 20"
            
            # Test Ollama connection
            if not self.generator.test_ollama_connection():
                return None, "❌ Cannot connect to Ollama. Please make sure Ollama is running with: ollama serve"
            
            # Process RAG context if enabled
            enhanced_prompt = prompt
            if use_rag:
                try:
                    print("🔍 Processing RAG context...")
                    
                    # Clear previous RAG cache
                    self.rag_processor.clear_cache()
                    
                    # Process uploaded files
                    if uploaded_files:
                        file_paths = [f.name for f in uploaded_files]
                        self.rag_processor.process_uploaded_files(file_paths)
                        print(f"Processed {len(file_paths)} uploaded files")
                    
                    # Process URLs
                    if urls_text and urls_text.strip():
                        urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
                        if urls:
                            self.rag_processor.process_urls(urls)
                            print(f"Processed {len(urls)} URLs")
                    
                    # Retrieve relevant context
                    if self.rag_processor.chunks:
                        relevant_chunks = self.rag_processor.retrieve_relevant_chunks(prompt, top_k=5)
                        enhanced_prompt = self.rag_processor.generate_context_prompt(prompt, relevant_chunks)
                        print(f"Enhanced prompt with {len(relevant_chunks)} relevant chunks")
                    else:
                        print("No RAG context found, using original prompt")
                        
                except Exception as e:
                    print(f"RAG processing error: {e}")
                    print("Continuing with original prompt...")
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.pptx', delete=False) as tmp_file:
                output_path = tmp_file.name
            
            # Update model if different
            if model_name != self.generator.ollama_client.model:
                self.generator.ollama_client.model = model_name
            
            # Generate presentation with enhanced prompt
            success = self.generator.generate_presentation(
                prompt=enhanced_prompt,
                output_file=output_path,
                num_slides=num_slides,
                enhance_content=enhance_content
            )
            
            if success:
                rag_status = " (with RAG context)" if use_rag and self.rag_processor.chunks else ""
                return output_path, f"✅ Presentation created successfully! ({num_slides} slides){rag_status}"
            else:
                return None, "❌ Failed to generate presentation"
                
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            print(f"Full error: {traceback.format_exc()}")
            return None, error_msg
    
    def improve_presentation_web(self, uploaded_ppt, model_name):
        """Improve existing PowerPoint presentation"""
        try:
            if not uploaded_ppt:
                return None, "❌ Please upload a PowerPoint file to improve"
            
            # Test Ollama connection
            if not self.generator.test_ollama_connection():
                return None, "❌ Cannot connect to Ollama. Please make sure Ollama is running with: ollama serve"
            
            # Create temporary output file
            with tempfile.NamedTemporaryFile(suffix='_improved.pptx', delete=False) as tmp_file:
                output_path = tmp_file.name
            
            # Improve the presentation
            improve_ppt(
                input_path=uploaded_ppt.name,
                output_path=output_path,
                outline_model=model_name,
                embed_model="nomic-embed-text"
            )
            
            return output_path, "✅ Presentation improved successfully! Content has been analyzed and enhanced."
                
        except Exception as e:
            error_msg = f"❌ Error improving presentation: {str(e)}"
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
            
            with gr.Tabs():
                # Tab 1: Create New Presentation
                with gr.Tab("📄 Create New Presentation"):
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
                                    label="AI Model",
                                    allow_custom_value=True
                                )
                            
                            enhance_input = gr.Checkbox(
                                value=True,
                                label="Enhance Content (more detailed but slower)"
                            )
                            
                            # RAG Section
                            with gr.Accordion("📚 RAG - Use Reference Materials", open=False):
                                gr.Markdown("Upload files (PPT, PDF, TXT) or provide URLs to use as context for your presentation")
                                
                                use_rag_input = gr.Checkbox(
                                    value=False,
                                    label="Enable RAG (Retrieval-Augmented Generation)"
                                )
                                
                                uploaded_files_input = gr.File(
                                    label="Upload Reference Files",
                                    file_count="multiple",
                                    file_types=[".pptx", ".pdf", ".txt", ".md"],
                                    visible=False
                                )
                                
                                urls_input = gr.Textbox(
                                    label="Reference URLs (one per line)",
                                    placeholder="https://example.com/article1\nhttps://example.com/article2",
                                    lines=3,
                                    visible=False
                                )
                                
                                # Show/hide RAG inputs based on checkbox
                                def toggle_rag_inputs(use_rag):
                                    return gr.update(visible=use_rag), gr.update(visible=use_rag)
                                
                                use_rag_input.change(
                                    fn=toggle_rag_inputs,
                                    inputs=[use_rag_input],
                                    outputs=[uploaded_files_input, urls_input]
                                )
                            
                            generate_btn = gr.Button("🚀 Generate Presentation", variant="primary", size="lg")
                        
                        with gr.Column(scale=1):
                            status_output = gr.Textbox(
                                label="Status",
                                interactive=False,
                                lines=5
                            )
                            
                            download_output = gr.File(
                                label="Download Presentation",
                                interactive=False
                            )
                            
                            # RAG Status
                            with gr.Accordion("📊 RAG Status", open=False):
                                gr.Markdown("Information about processed reference materials will appear here")
                
                # Tab 2: Improve Existing Presentation
                with gr.Tab("🔧 Improve Existing Presentation"):
                    with gr.Row():
                        with gr.Column(scale=2):
                            gr.Markdown("### Upload an existing PowerPoint to analyze and improve")
                            gr.Markdown("The AI will analyze your presentation, remove redundancy, improve structure, and enhance clarity.")
                            
                            ppt_upload_input = gr.File(
                                label="Upload PowerPoint File",
                                file_types=[".pptx"],
                                file_count="single"
                            )
                            
                            improve_model_input = gr.Dropdown(
                                choices=available_models,
                                value=available_models[0],
                                label="AI Model for Analysis",
                                allow_custom_value=True
                            )
                            
                            improve_btn = gr.Button("🔧 Improve Presentation", variant="primary", size="lg")
                        
                        with gr.Column(scale=1):
                            improve_status_output = gr.Textbox(
                                label="Status",
                                interactive=False,
                                lines=5
                            )
                            
                            improve_download_output = gr.File(
                                label="Download Improved Presentation",
                                interactive=False
                            )
                            
                            with gr.Accordion("ℹ️ How it works", open=False):
                                gr.Markdown("""
                                **The improvement process:**
                                1. Extracts content from all slides
                                2. Removes duplicate or redundant information
                                3. Uses AI to reorganize and enhance structure
                                4. Creates cleaner, more concise bullet points
                                5. Generates a new presentation with improved flow
                                """)
            
            # Setup event handlers
            generate_btn.click(
                fn=self.generate_presentation_web,
                inputs=[
                    prompt_input, 
                    slides_input, 
                    model_input, 
                    enhance_input,
                    uploaded_files_input,
                    urls_input,
                    use_rag_input
                ],
                outputs=[download_output, status_output]
            )
            
            improve_btn.click(
                fn=self.improve_presentation_web,
                inputs=[ppt_upload_input, improve_model_input],
                outputs=[improve_download_output, improve_status_output]
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
        server_name="localhost",  # Allow external access
        server_port=7860,
        share=True,  # Create public link
        show_error=True
    )


if __name__ == "__main__":
    main()
