import gradio as gr
import os
import tempfile
from ppt_generator import PPTGenerator
from rag_processor import RAGProcessor
from ppt_improver import improve_ppt
from ai_client_manager import AIClientManager, get_client_info
from config import DEFAULT_MODEL, AI_PROVIDERS, DEFAULT_AI_PROVIDER, get_timestamped_filename, get_improved_filename
import traceback

class PPTMakerWeb:
    def __init__(self, ai_provider=None):
        # Initialize with auto-detection or specified provider
        if ai_provider:
            self.generator = PPTGenerator(ai_provider=ai_provider)
        else:
            # Auto-detect best available provider
            self.generator = PPTGenerator()
            
        self.rag_processor = RAGProcessor()
        
        # Get AI client info for display
        self.ai_info = get_client_info(self.generator.ai_client)
    
    def get_ai_provider_info(self):
        """Get information about current AI provider"""
        return f"🤖 AI Provider: {self.ai_info['provider'].title()} {'✅' if self.ai_info['connected'] else '❌'}"
    
    def get_available_models(self):
        """Get list of available models"""
        try:
            return self.generator.list_available_models()
        except:
            return [DEFAULT_MODEL]
    
    def generate_presentation_web(self, prompt, num_slides, model_name, enhance_content, uploaded_files, urls_text, use_rag):
        """Generate presentation through web interface"""
        try:
            if not prompt.strip():
                return None, "❌ Please enter a presentation topic"
            
            if num_slides < 2 or num_slides > 20:
                return None, "❌ Number of slides must be between 2 and 20"
            
            # Test AI service connection
            if not self.generator.test_connection():
                return None, "❌ Cannot connect to AI service. Please check that your AI service is running."
            
            # Process uploaded reference materials if enabled
            enhanced_prompt = prompt
            if use_rag:
                try:
                    print("🔍 Processing uploaded reference materials...")
                    
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
                        print("No reference content found, using original prompt")
                        
                except Exception as e:
                    print(f"Reference processing error: {e}")
                    print("Continuing with original prompt...")
            
            # Create temporary file with timestamped name
            timestamped_name = get_timestamped_filename("presentation")
            with tempfile.NamedTemporaryFile(suffix='.pptx', delete=False) as tmp_file:
                output_path = tmp_file.name
            
            # Rename to have a meaningful timestamped name for download
            meaningful_path = os.path.join(os.path.dirname(output_path), timestamped_name)
            
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
                # Rename to meaningful timestamped name
                try:
                    os.rename(output_path, meaningful_path)
                    output_path = meaningful_path
                except:
                    pass  # If rename fails, use original temp path
                
                rag_status = " (using uploaded references)" if use_rag and self.rag_processor.chunks else ""
                return output_path, f"✅ Presentation created successfully! ({num_slides} slides){rag_status}\n📁 File: {os.path.basename(output_path)}"
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
            
            # Create temporary output file with meaningful name
            improved_name = get_improved_filename(uploaded_ppt.name)
            with tempfile.NamedTemporaryFile(suffix='_improved.pptx', delete=False) as tmp_file:
                output_path = tmp_file.name
            
            # Rename to have a meaningful timestamped name for download
            meaningful_path = os.path.join(os.path.dirname(output_path), improved_name)
            
            # Improve the presentation
            improve_ppt(
                input_path=uploaded_ppt.name,
                output_path=output_path,
                outline_model=model_name,
                embed_model="nomic-embed-text"
            )
            
            # Rename to meaningful timestamped name
            try:
                os.rename(output_path, meaningful_path)
                output_path = meaningful_path
            except:
                pass  # If rename fails, use original temp path
            
            return output_path, f"✅ Presentation improved successfully! Content has been analyzed and enhanced.\n📁 File: {os.path.basename(output_path)}"
                
        except Exception as e:
            error_msg = f"❌ Error improving presentation: {str(e)}"
            print(f"Full error: {traceback.format_exc()}")
            return None, error_msg
    
    def get_available_models(self):
        """Get list of available Ollama models"""
        try:
            models = self.generator.list_available_models()
            if models:
                # Ensure default model is first in the list
                if DEFAULT_MODEL in models:
                    models.remove(DEFAULT_MODEL)
                    models.insert(0, DEFAULT_MODEL)
                return models
            else:
                return [DEFAULT_MODEL, "llama3", "mistral"]
        except:
            return [DEFAULT_MODEL, "llama3", "mistral"]
    
    def create_interface(self):
        """Create Gradio web interface"""
        
        # Get available models
        available_models = self.get_available_models()
        
        with gr.Blocks(title="PPT Maker", theme=gr.themes.Soft()) as interface:
            gr.Markdown("# 🎯 PPT Maker")
            gr.Markdown("Generate professional PowerPoint presentations from text prompts using AI")
            gr.Markdown(f"**Default AI Model:** {DEFAULT_MODEL} | **Embedding Model:** nomic-embed-text")
            gr.Markdown(f"**{self.get_ai_provider_info()}**")
            
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
                                    label=f"AI Model (Default: {DEFAULT_MODEL})",
                                    allow_custom_value=True
                                )
                            
                            enhance_input = gr.Checkbox(
                                value=True,
                                label="Enhance Content (more detailed but slower)"
                            )
                            
                            # Reference Materials Section
                            with gr.Accordion("📚 Upload Layout or Old PPT for Reference", open=False):
                                gr.Markdown("Upload existing presentations, templates, or documents to use as inspiration and context for your new presentation")
                                
                                use_rag_input = gr.Checkbox(
                                    value=False,
                                    label="Use uploaded files/URLs as reference"
                                )
                                
                                uploaded_files_input = gr.File(
                                    label="Upload Layout/Template Files (PPT, PDF, TXT)",
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
                                
                                # Show/hide reference upload inputs based on checkbox
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
                                label=f"AI Model for Analysis (Default: {DEFAULT_MODEL})",
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
                
                # Tab 3: Configuration & Settings
                with gr.Tab("⚙️ Configuration"):
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### Current Configuration")
                            gr.Markdown(f"""
                            **Default Settings:**
                            - **Text Generation Model:** `{DEFAULT_MODEL}`
                            - **Embedding Model:** `nomic-embed-text`
                            - **Default Slides:** 8
                            - **Max Slides:** 20
                            - **Ollama URL:** http://localhost:11434
                            
                            **Available Models:**
                            """)
                            
                            def get_model_list():
                                try:
                                    models = self.generator.list_available_models()
                                    if models:
                                        model_text = "\n".join([f"- {model} {'(Default)' if model == DEFAULT_MODEL else ''}" for model in models])
                                        return f"**Installed Models:**\n{model_text}"
                                    else:
                                        return "**No models found** - Please ensure Ollama is running"
                                except:
                                    return "**Error connecting to Ollama** - Please check your setup"
                            
                            model_status = gr.Markdown(get_model_list())
                            
                            refresh_btn = gr.Button("🔄 Refresh Model List", variant="secondary")
                            
                            def refresh_models():
                                return get_model_list()
                            
                            refresh_btn.click(fn=refresh_models, outputs=[model_status])
                        
                        with gr.Column():
                            gr.Markdown("### How to Change Models")
                            gr.Markdown("""
                            **To use different models:**
                            
                            **In Web Interface:**
                            - Select different models from the dropdown in Create/Improve tabs
                            - Models are automatically detected from your Ollama installation
                            
                            **Via Command Line:**
                            ```bash
                            # Use custom model for generation
                            python ppt_maker.py "topic" --model llama3
                            
                            # Use custom model for improvement
                            python ppt_improver.py input.pptx output.pptx --outline-model mistral
                            
                            # List available models
                            python ppt_maker.py --list-models
                            ```
                            
                            **Install New Models:**
                            ```bash
                            ollama pull model-name
                            ollama list  # verify installation
                            ```
                            
                            **Supported Model Types:**
                            - **Text Generation:** llama3, mistral, codellama, etc.
                            - **Embeddings:** nomic-embed-text, all-minilm, etc.
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
        server_port=7861,
        share=True,  # Create public link
        show_error=True
    )


if __name__ == "__main__":
    main()
