# PPT Maker

A comprehensive Python application that generates and improves PowerPoint presentations using AI. Features include text-to-PPT generation, reference material integration, presentation improvement capabilities, and support for multiple AI providers.

## 🚀 Features

### Core Features
- **🤖 Multi-AI Provider Support**: Works with both Ollama and LM Studio
- **📝 AI-Powered Generation**: Create presentations from natural language prompts
- **📚 Reference Material Integration**: Use existing presentations, PDFs, documents, and URLs as inspiration
- **🔧 Presentation Improvement**: Analyze and enhance existing PowerPoint files
- **🌐 Web Interface**: User-friendly Gradio-based web application with tabbed interface
- **💻 Command Line Interface**: Full CLI access for automation and scripting
- **⏰ Timestamped Outputs**: Automatic timestamp generation for organized file management
- **🎯 Smart Model Selection**: Automatic detection and selection of best available AI models

### AI Provider Support
- **LM Studio**: User-friendly GUI-based local AI with OpenAI-compatible API
- **Ollama**: Command-line AI service with extensive model library
- **Auto-Detection**: Automatically detects and uses the best available provider
- **Manual Override**: Explicitly choose your preferred AI provider

### Reference Material Integration (formerly RAG)
- **📊 Upload Layout/Old PPT**: Use existing presentations as templates and inspiration
- **📄 Document Processing**: Support for PowerPoint (.pptx), PDF (.pdf), and text files (.txt, .md)
- **🌐 Web Content**: Fetch and process content from URLs
- **🧠 Smart Context**: Intelligent chunking and similarity-based content retrieval
- **✨ Enhanced Generation**: Context-aware presentation creation

### Presentation Improvement
- **🔍 Content Analysis**: Deep analysis of existing presentations
- **🗑️ Deduplication**: Remove redundant and duplicate content using AI embeddings
- **📈 Structure Enhancement**: AI-powered content reorganization and flow improvement
- **🎨 Layout Optimization**: Better slide structure and content distribution

## 📋 Prerequisites

### AI Provider (Choose One or Both)

#### Option 1: LM Studio (Recommended for Beginners)
- Download from [lmstudio.ai](https://lmstudio.ai)
- User-friendly GUI interface
- Easy model management
- No command-line experience required

#### Option 2: Ollama (Advanced Users)
- Download from [ollama.com](https://ollama.com)
- Command-line based
- Extensive model library
- More technical control

### System Requirements
- **Python 3.7+**
- **RAM**: 8GB minimum (16GB recommended for larger models)
- **Storage**: 5-50GB for AI models (depending on size)
- **OS**: Windows, macOS, or Linux

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/studentGarv/PPT-Maker.git
cd PPT-Maker
```

### 2. Install Python Dependencies
```bash
# Install core dependencies
pip install -r requirements.txt

# For web interface (optional)
pip install -r requirements_web.txt
```

### 3. Setup AI Provider

#### Option A: LM Studio Setup (Easier)
1. Download and install LM Studio from [lmstudio.ai](https://lmstudio.ai)
2. Launch LM Studio
3. Go to **Search** tab and download the models(gpt-oss:20b and nomic-embed-text)
4. Go to **Chat** tab and load your downloaded model 
5. Go to **Local Server** tab and click **Start Server**
6. ✅ PPT Maker will auto-detect LM Studio!

#### Option B: Ollama Setup (Advanced)
```bash
# Install Ollama (visit https://ollama.com for platform-specific instructions)

# Pull required models
ollama pull gpt-oss:20b
ollama pull nomic-embed-text

# Optional additional models
ollama pull llama3
ollama pull mistral

# Start Ollama server
ollama serve
```

### 4. Test Your Setup
```bash
# Test AI provider connection
python ppt_maker.py --test-connection

# Run interactive demo
python test_lm_studio.py  # For LM Studio
python ppt_maker.py --test-connection --provider ollama  # For Ollama
```

## 🎯 Usage

### 🌐 Web Interface (Recommended for Most Users)
```bash
# Start the web application
python web_app.py

# Access at: http://localhost:7861
```

#### Web Interface Features:
- **📄 Create New Presentation Tab**:
  - Enter presentation topic
  - Configure slides and AI model
  - Upload layout/template files or old presentations for reference
  - Add reference URLs for additional context
  - Generate presentations with automatic timestamped filenames

- **🔧 Improve Existing Presentation Tab**:
  - Upload existing PowerPoint files
  - AI-powered analysis and enhancement
  - Remove duplicate content automatically
  - Download improved presentations with timestamps

- **⚙️ Configuration Tab**:
  - View current AI provider status
  - See available models
  - Monitor system status

### 💻 Command Line Interface

#### Basic Presentation Generation
```bash
# Simple generation (auto-detects best AI provider and generates timestamped file)
python ppt_maker.py "Create a presentation about artificial intelligence"

# Specify AI provider
python ppt_maker.py "Business strategy overview" --provider lm_studio
python ppt_maker.py "Data analysis" --provider ollama

# Specify number of slides
python ppt_maker.py "Business strategy overview" --slides 10

# Custom output file (overrides automatic timestamping)
python ppt_maker.py "Data science fundamentals" --output "data_science.pptx"

# Use specific AI model
python ppt_maker.py "Climate change solutions" --model "meta-llama-3.1-8b-instruct"

# Disable content enhancement for faster generation
python ppt_maker.py "Quick company overview" --no-enhance

# Verbose output for debugging
python ppt_maker.py "Detailed analysis" --verbose
```

#### AI Provider and Model Management
```bash
# Test connection (auto-detects providers)
python ppt_maker.py --test-connection

# Test specific provider
python ppt_maker.py --test-connection --provider lm_studio
python ppt_maker.py --test-connection --provider ollama

# List available models from current provider
python ppt_maker.py --list-models

# List models from specific provider
python ppt_maker.py --list-models --provider lm_studio

# Use custom API endpoint
python ppt_maker.py "Topic" --provider lm_studio --base-url "http://localhost:1234"
```

#### Presentation Improvement
```bash
# Improve existing presentation (auto-generates timestamped output)
python ppt_improver.py input.pptx

# Specify output file
python ppt_improver.py input.pptx output_improved.pptx

# With custom models and settings
python ppt_improver.py input.pptx output.pptx --outline-model llama3 --embed-model nomic-embed-text

# With custom threshold and verbose output
python ppt_improver.py input.pptx output.pptx --threshold 0.9 --verbose

# Using a template
python ppt_improver.py input.pptx output.pptx --template custom_template.pptx
```

#### Testing and Diagnostics
```bash
# Test LM Studio integration
python test_lm_studio.py

# Interactive model selection demo
python model_selection_demo.py

# See model recommendations
python model_selection_demo.py --recommendations

# Interactive model testing
python model_selection_demo.py --interactive
```

### 🐍 Python API Usage

#### Basic Generation with Auto-Detection
```python
from ppt_generator import PPTGenerator

# Auto-detects best available AI provider
generator = PPTGenerator()
success = generator.generate_presentation(
    prompt="Artificial Intelligence in Healthcare",
    output_file="ai_healthcare.pptx",  # Or None for auto-timestamped
    num_slides=8,
    enhance_content=True
)
```

#### Specify AI Provider
```python
from ppt_generator import PPTGenerator

# Use LM Studio explicitly
generator = PPTGenerator(ai_provider="lm_studio")

# Use Ollama explicitly  
generator = PPTGenerator(ai_provider="ollama", model="gpt-oss:20b")

# Use custom endpoint
generator = PPTGenerator(
    ai_provider="lm_studio",
    base_url="http://localhost:1234"
)
```

#### Reference Material Integration
```python
from rag_processor import RAGProcessor
from ppt_generator import PPTGenerator

# Setup reference material processor
rag = RAGProcessor()
rag.process_uploaded_files(["existing_presentation.pptx", "research.pdf"])
rag.process_urls(["https://example.com/article"])

# Generate enhanced prompt
relevant_chunks = rag.retrieve_relevant_chunks("AI in healthcare", top_k=5)
enhanced_prompt = rag.generate_context_prompt("AI in healthcare", relevant_chunks)

# Generate presentation with context
generator = PPTGenerator()
generator.generate_presentation(enhanced_prompt, "enhanced_ai.pptx")
```

#### Presentation Improvement
```python
from ppt_improver import improve_ppt

improve_ppt(
    input_path="old_presentation.pptx",
    output_path="improved_presentation.pptx",  # Or None for auto-timestamped
    outline_model="gpt-oss:20b",
    embed_model="nomic-embed-text"
)
```

#### AI Client Management
```python
from ai_client_manager import AIClientManager

# Auto-detect best provider
client = AIClientManager.auto_detect_provider()
print(f"Using provider: {client.provider}")

# Use specific provider
lm_client = AIClientManager.create_client("lm_studio")
ollama_client = AIClientManager.create_client("ollama", model="llama3")

# Generate content
outline = client.generate_presentation_outline("Machine Learning Basics", 5)
```

## 🔧 Configuration

### AI Provider Configuration (`config.py`)
```python
# AI Provider settings
AI_PROVIDERS = {
    "ollama": {
        "name": "Ollama",
        "base_url": "http://localhost:11434",
        "default_model": "gpt-oss:20b"
    },
    "lm_studio": {
        "name": "LM Studio", 
        "base_url": "http://localhost:1234",
        "default_model": None  # Uses loaded model
    }
}

# Default AI provider (auto-detects if not specified)
DEFAULT_AI_PROVIDER = "ollama"
```

### Presentation Settings
```python
# Presentation configuration
DEFAULT_SLIDES_COUNT = 8
MAX_SLIDES_COUNT = 20
MIN_SLIDES_COUNT = 2

# Output settings (automatic timestamping)
get_timestamped_filename("presentation")  # presentation_20250903_140530.pptx
get_improved_filename("input.pptx")       # input_improved_20250903_140530.pptx
```

### Available Models by Provider

#### LM Studio Models (Examples)
- **meta-llama-3.1-8b-instruct** (Recommended for presentations)
- **mistral-7b-instruct** (Good balance of speed/quality)
- **qwen2.5-7b-instruct** (Creative content)
- **phi-3-mini** (Fast, lightweight)

#### Ollama Models  
- **gpt-oss:20b** (Default, high quality)
- **llama3** (Fast, reliable)
- **mistral** (Creative, detailed)
- **nomic-embed-text** (For embeddings/similarity)

## 📁 Project Structure

```
PPT-Maker/
├── 🌐 Web Interface
│   └── web_app.py              # Gradio web interface with tabs
├── 💻 Command Line Tools  
│   ├── ppt_maker.py            # Main CLI application
│   └── ppt_improver.py         # Presentation improvement CLI
├── 🤖 AI Integration
│   ├── ai_client_manager.py    # Multi-provider AI client manager
│   ├── ollama_client.py        # Ollama API client
│   ├── lm_studio_client.py     # LM Studio API client  
│   └── config.py              # AI provider configuration
├── 🧠 Core Logic
│   ├── ppt_generator.py        # Core PPT generation logic
│   ├── pptx_generator.py       # PowerPoint file creation
│   └── rag_processor.py        # Reference material processing
├── 🧪 Testing & Demo
│   ├── test_lm_studio.py       # LM Studio integration test
│   ├── model_selection_demo.py # Model selection demonstration
│   └── test_ppt_maker.py       # Unit tests
├── 📚 Documentation
│   ├── README.md              # This file
│   ├── LM_STUDIO_GUIDE.md     # LM Studio setup guide
│   ├── RAG_FEATURES.md        # Reference material features
│   └── DEPLOYMENT.md          # Deployment instructions
├── 📦 Dependencies
│   ├── requirements.txt       # Core Python dependencies
│   └── requirements_web.txt   # Web interface dependencies
└── 🛠️ Build Tools
    ├── build_executable.bat   # Windows executable builder
    └── create_portable.bat    # Portable version creator
```

## 🐛 Troubleshooting

### AI Provider Issues

#### LM Studio Problems
```bash
# Check LM Studio status
python test_lm_studio.py

# Common solutions:
# 1. Ensure LM Studio app is running
# 2. Load a model in the Chat tab
# 3. Start Local Server (port 1234)
# 4. Check firewall settings
```

#### Ollama Problems  
```bash
# Check Ollama status
python ppt_maker.py --test-connection --provider ollama

# Common solutions:
ollama serve          # Start Ollama server
ollama list           # Check available models  
ollama pull llama3    # Download missing models
```

#### Auto-Detection Issues
```bash
# Force specific provider
python ppt_maker.py "Topic" --provider lm_studio
python ppt_maker.py "Topic" --provider ollama

# Check what's detected
python model_selection_demo.py
```

### Common Issues

1. **"Cannot connect to AI service"**
```bash
# Test connections
python ppt_maker.py --test-connection

# Check specific provider
python test_lm_studio.py
ollama list
```

2. **"No models found"**
```bash
# For LM Studio: Load a model in the app
# For Ollama: Pull models
ollama pull gpt-oss:20b
ollama pull nomic-embed-text
```

3. **Dependencies Issues**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# For web interface
pip install -r requirements_web.txt

# For PDF support
pip install PyPDF2
```

4. **Port Conflicts**
```bash
# LM Studio default: localhost:1234  
# Ollama default: localhost:11434
# Web app: localhost:7861

# Use custom ports
python ppt_maker.py "Topic" --base-url "http://localhost:9999"
```

5. **Memory/Performance Issues**
```bash
# Use smaller models
python ppt_maker.py "Topic" --model "phi-3-mini"

# Disable content enhancement  
python ppt_maker.py "Topic" --no-enhance

# Use fewer slides
python ppt_maker.py "Topic" --slides 5
```

### File Output Issues

6. **Timestamp Format**
```bash
# Default format: presentation_20250903_140530.pptx
# Improved format: input_improved_20250903_140530.pptx

# Override with custom name
python ppt_maker.py "Topic" --output "custom_name.pptx"
```

## 🚀 Advanced Usage

### Multi-Provider Workflow
```bash
# Compare providers for same topic
python ppt_maker.py "AI Ethics" --provider lm_studio --output "ai_ethics_lm.pptx"
python ppt_maker.py "AI Ethics" --provider ollama --output "ai_ethics_ollama.pptx"
```

### Reference Material Integration
```python
# Advanced reference processing
from rag_processor import RAGProcessor

rag = RAGProcessor()

# Process multiple file types
rag.process_uploaded_files([
    "company_template.pptx",    # Use as layout reference
    "research_paper.pdf",       # Content reference  
    "notes.txt"                 # Additional context
])

# Add web sources
rag.process_urls([
    "https://example.com/latest-trends",
    "https://research.org/white-paper"
])

# Generate with rich context
relevant_context = rag.retrieve_relevant_chunks("your topic", top_k=10)
enhanced_prompt = rag.generate_context_prompt("your topic", relevant_context)
```

### Batch Processing
```python
# Generate multiple presentations
topics = [
    "Q1 Financial Results",
    "Marketing Strategy 2024", 
    "Product Roadmap Update"
]

from ppt_generator import PPTGenerator
generator = PPTGenerator()

for topic in topics:
    generator.generate_presentation(
        prompt=topic,
        output_file=None,  # Auto-timestamped
        num_slides=6
    )
```

### Custom Model Selection
```python
# Advanced model selection
from lm_studio_client import LMStudioClient

client = LMStudioClient()
available_models = client.get_available_models()
best_model = client.select_best_model()

print(f"Best model for presentations: {best_model}")

# Use specific model
client_with_model = LMStudioClient(model="meta-llama-3.1-8b-instruct")
```

### Template-Based Generation
```python
# Use existing presentation as template
generator.generate_presentation(
    prompt="New Product Launch",
    template_path="company_template.pptx",
    output_file="product_launch.pptx"
)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes and add tests
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Submit a pull request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/PPT-Maker.git
cd PPT-Maker

# Create development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
pip install -r requirements.txt
pip install -r requirements_web.txt

# Run tests
python -m pytest tests/
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support & Resources

### Getting Help
- 🐛 **Issues**: [GitHub Issues](https://github.com/studentGarv/PPT-Maker/issues)
- 📖 **Documentation**: Check the guides in the repository
- 💬 **Discussions**: Use GitHub Discussions for questions

### Additional Resources  
- 📚 **LM Studio Guide**: `LM_STUDIO_GUIDE.md` - Complete LM Studio setup
- 🔍 **Reference Features**: `RAG_FEATURES.md` - Advanced reference material usage  
- 🚀 **Deployment**: `DEPLOYMENT.md` - Production deployment guide
- 🧪 **Testing**: Run `python test_lm_studio.py` and `python model_selection_demo.py`

### Quick Start Examples
```bash
# Absolute beginner
python web_app.py                    # Start web interface

# Command line user  
python ppt_maker.py "Your topic"     # Generate with auto-detection

# Advanced user
python model_selection_demo.py       # Explore model options
python test_lm_studio.py            # Test LM Studio integration
```

---

**🎯 PPT Maker - Transform your ideas into professional presentations with AI!**