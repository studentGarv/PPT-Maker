# PPT Maker

A comprehensive Python application that generates and improves PowerPoint presentations using AI. Features include text-to-PPT generation, RAG (Retrieval-Augmented Generation) with multiple document types, and presentation improvement capabilities.

## 🚀 Features

### Core Features
- **AI-Powered Generation**: Create presentations from natural language prompts
- **RAG Support**: Use reference materials (PPT, PDF, TXT, URLs) as context
- **Presentation Improvement**: Analyze and enhance existing PowerPoint files
- **Web Interface**: User-friendly Gradio-based web application
- **Command Line Interface**: Direct CLI access for automation
- **Multiple AI Models**: Support for various Ollama models

### RAG (Retrieval-Augmented Generation)
- Upload PowerPoint files (.pptx) for context
- Process PDF documents (.pdf) 
- Include text files (.txt, .md)
- Fetch content from web URLs
- Intelligent content chunking and similarity search
- Context-aware presentation generation

### Presentation Improvement
- Analyze existing presentations
- Remove duplicate/redundant content
- AI-powered content reorganization
- Enhanced structure and flow
- Embedding-based deduplication

## 📋 Prerequisites

- Python 3.7+
- Ollama installed and running locally
- Required Ollama models (llama3, nomic-embed-text)

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/studentGarv/PPT-Maker.git
cd PPT-Maker
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install and setup Ollama**
```bash
# Install Ollama (visit https://ollama.ai for platform-specific instructions)

# Pull required models
ollama pull llama3
ollama pull nomic-embed-text
ollama pull mistral

# Start Ollama server
ollama serve
```

## 🎯 Usage

### Web Interface (Recommended)
```bash
# Start the web application
python web_app.py

# Access at: http://localhost:7860
```

#### Web Interface Features:
- **Create New Presentation Tab**:
  - Enter presentation topic
  - Configure slides and AI model
  - Enable RAG with file uploads or URLs
  - Generate context-aware presentations

- **Improve Existing Presentation Tab**:
  - Upload existing PowerPoint files
  - AI-powered analysis and enhancement
  - Download improved presentations

### Command Line Interface

#### Basic Presentation Generation
```bash
# Simple generation
python ppt_maker.py "Create a presentation about artificial intelligence"

# Specify number of slides
python ppt_maker.py "Business strategy overview" --slides 10

# Custom output file
python ppt_maker.py "Data science fundamentals" --output "data_science.pptx"

# Use different AI model
python ppt_maker.py "Climate change solutions" --model "mistral"

# Disable content enhancement for faster generation
python ppt_maker.py "Quick company overview" --no-enhance

# Verbose output for debugging
python ppt_maker.py "Detailed analysis" --verbose
```

#### Testing and Diagnostics
```bash
# Test Ollama connection
python ppt_maker.py --test-connection

# List available models
python ppt_maker.py --list-models

# Check system status
python ppt_maker.py --status
```

#### Presentation Improvement
```bash
# Improve existing presentation
python ppt_improver.py input.pptx output_improved.pptx

# With custom models
python ppt_improver.py input.pptx output.pptx --outline-model llama3 --embed-model nomic-embed-text
```

#### RAG Processing
```bash
# Test RAG processor
python rag_processor.py

# Process specific files (programmatic usage)
from rag_processor import RAGProcessor
processor = RAGProcessor()
processor.process_uploaded_files(["doc1.pdf", "doc2.pptx"])
```

### Python API Usage

#### Basic Generation
```python
from ppt_generator import PPTGenerator

generator = PPTGenerator(model="llama3")
success = generator.generate_presentation(
    prompt="Artificial Intelligence in Healthcare",
    output_file="ai_healthcare.pptx",
    num_slides=8,
    enhance_content=True
)
```

#### RAG-Enhanced Generation
```python
from rag_processor import RAGProcessor
from ppt_generator import PPTGenerator

# Setup RAG
rag = RAGProcessor()
rag.process_uploaded_files(["research.pdf", "existing.pptx"])
rag.process_urls(["https://example.com/article"])

# Generate enhanced prompt
relevant_chunks = rag.retrieve_relevant_chunks("AI in healthcare", top_k=5)
enhanced_prompt = rag.generate_context_prompt("AI in healthcare", relevant_chunks)

# Generate presentation
generator = PPTGenerator()
generator.generate_presentation(enhanced_prompt, "enhanced_ai.pptx")
```

#### Presentation Improvement
```python
from ppt_improver import improve_ppt

improve_ppt(
    input_path="old_presentation.pptx",
    output_path="improved_presentation.pptx",
    outline_model="llama3",
    embed_model="nomic-embed-text"
)
```

## 🔧 Configuration

### Environment Configuration (`config.py`)
```python
# Customize default settings
DEFAULT_SLIDES_COUNT = 8
MAX_SLIDES_COUNT = 20
MIN_SLIDES_COUNT = 2
DEFAULT_OUTPUT_FILE = "presentation.pptx"
OLLAMA_BASE_URL = "http://localhost:11434"
```

### Available Models
- **Text Generation**: llama3, mistral, llama2, codellama
- **Embeddings**: nomic-embed-text, all-minilm
- **Custom Models**: Any Ollama-compatible model

## 📁 Project Structure

```
PPT-Maker/
├── web_app.py              # Gradio web interface
├── ppt_maker.py            # Main CLI application
├── ppt_generator.py        # Core PPT generation logic
├── ppt_improver.py         # Presentation improvement
├── rag_processor.py        # RAG functionality
├── ollama_client.py        # Ollama API client
├── pptx_generator.py       # PowerPoint file creation
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── requirements_web.txt   # Web interface dependencies
├── README.md             # This file
├── RAG_FEATURES.md       # RAG documentation
└── tests/
    └── test_ppt_maker.py  # Unit tests
```

## 🐛 Troubleshooting

### Common Issues

1. **Ollama Connection Failed**
```bash
# Check if Ollama is running
ollama list

# Start Ollama server
ollama serve

# Test connection
python ppt_maker.py --test-connection
```

2. **Model Not Found**
```bash
# List available models
ollama list

# Pull missing model
ollama pull llama3
```

3. **Dependencies Issues**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# For web interface
pip install -r requirements_web.txt
```

4. **PDF Processing Issues**
```bash
# Install PDF support
pip install PyPDF2

# Alternative PDF library
pip install pypdf
```

## 🚀 Advanced Usage

### Batch Processing
```bash
# Process multiple topics
python ppt_maker.py "Topic 1" "Topic 2" "Topic 3" --batch

# From file list
python ppt_maker.py --topics-file topics.txt
```

### Custom Templates
```python
# Use custom PowerPoint template
generator.generate_presentation(
    prompt="Business Quarterly Review",
    template_path="custom_template.pptx",
    output_file="quarterly_review.pptx"
)
```

### Export Options
```bash
# Export with different formats (if supported)
python ppt_maker.py "Topic" --export-pdf --export-images
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

- Create an issue on GitHub
- Check the troubleshooting section
- Review the RAG_FEATURES.md for advanced usage