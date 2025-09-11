# PPT Maker
A comprehensive Python application that generates and improves PowerPoint presentations using AI. Features include text-to-PPT generation, reference material integration, presentation improvement capabilities, and support for multiple AI providers.

## 🚀 Features

- **📝 AI-Powered Generation**: Create presentations from natural language prompts
- **📊 Upload Layout/Old PPT**: Use existing presentations, PDFs, documents, and URLs as inspiration
- **🔧 Presentation Improvement**: Analyze and enhance existing PowerPoint files
- **🌐 Web Interface**: User-friendly Gradio-based web application with tabbed interface
- **💻 Command Line Interface**: Full CLI access for automation and scripting

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

# For web interface
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
# Install Ollama (visit https://ollama.com )

# Pull required models
ollama pull gpt-oss:20b
ollama pull nomic-embed-text

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
  - Upload old presentations for reference
  - Add reference URLs for additional context
  - Generate presentations 

- **🔧 Improve Existing Presentation Tab**:
  - Upload existing PowerPoint files
  - AI-powered analysis and enhancement
  - Remove duplicate content automatically
  - Download improved presentations 

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

**🎯 PPT Maker - Transform your ideas into professional presentations with AI!**