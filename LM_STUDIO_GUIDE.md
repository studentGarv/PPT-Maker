# LM Studio Integration Guide

## Overview

PPT Maker now supports **LM Studio** as an alternative to Ollama for AI-powered presentation generation. LM Studio provides a user-friendly way to run large language models locally with an OpenAI-compatible API.

## What is LM Studio?

LM Studio is a desktop application that allows you to run large language models locally on your machine. It provides:

- Easy model downloading and management
- User-friendly chat interface
- Local OpenAI-compatible API server
- Support for various model formats (GGUF, GGML)
- No internet connection required for inference

## Setup Instructions

### 1. Install LM Studio

1. Download LM Studio from [https://lmstudio.ai/](https://lmstudio.ai/)
2. Install the application on your system (Windows, macOS, or Linux)
3. Launch LM Studio

### 2. Download a Model

1. In LM Studio, go to the **Search** tab
2. Search for a model (recommended: "Llama 3.1 8B" or "Mistral 7B")
3. Click **Download** on your chosen model
4. Wait for the download to complete

### 3. Load and Start the Model

1. Go to the **Chat** tab
2. Select your downloaded model from the dropdown
3. Click **Load Model**
4. Go to the **Local Server** tab
5. Click **Start Server** (default port: 1234)
6. Ensure the server status shows "Running"

### 4. Configure PPT Maker

PPT Maker will automatically detect and use LM Studio if it's running. You can also explicitly specify LM Studio:

#### Command Line
```bash
# Auto-detect (tries LM Studio first, then Ollama)
python ppt_maker.py "Your presentation topic"

# Explicitly use LM Studio
python ppt_maker.py "Your presentation topic" --provider lm_studio

# Use custom URL
python ppt_maker.py "Your presentation topic" --provider lm_studio --base-url http://localhost:1234
```

#### Web Interface
The web app will automatically detect and display the active AI provider at the top of the interface.

## Usage Examples

### Basic Presentation Generation
```bash
python ppt_maker.py "Artificial Intelligence in Healthcare" --provider lm_studio
```

### With Custom Settings
```bash
python ppt_maker.py "Machine Learning Basics" \
  --provider lm_studio \
  --slides 10 \
  --output "ml_basics.pptx" \
  --base-url http://localhost:1234
```

### Test Connection
```bash
python ppt_maker.py --test-connection --provider lm_studio
```

### List Available Models
```bash
python ppt_maker.py --list-models --provider lm_studio
```

## Configuration

### Default Settings

LM Studio settings in `config.py`:
```python
AI_PROVIDERS = {
    "lm_studio": {
        "name": "LM Studio", 
        "base_url": "http://localhost:1234",
        "default_model": None  # Uses loaded model
    }
}
```

### Auto-Detection Priority

PPT Maker will automatically try providers in this order:
1. **LM Studio** (port 1234)
2. **Ollama** (port 11434)

If both are running, LM Studio takes priority.

## API Compatibility

LM Studio provides an OpenAI-compatible API, which means:

- Familiar API structure for developers
- Easy integration with existing OpenAI code
- Standard request/response format
- Support for chat completions and embeddings (if model supports it)

## Troubleshooting

### Common Issues

#### 1. "Cannot connect to LM Studio"
- ✅ Ensure LM Studio is running
- ✅ Check that Local Server is started (port 1234)
- ✅ Verify a model is loaded in the Chat tab
- ✅ Check firewall settings

#### 2. "No models found"
- ✅ Load a model in LM Studio's Chat tab
- ✅ Ensure the model is compatible (chat/instruct models work best)
- ✅ Try restarting the Local Server

#### 3. "Generation fails or produces poor results"
- ✅ Try a different model (larger models often perform better)
- ✅ Adjust model parameters in LM Studio (temperature, context length)
- ✅ Ensure sufficient system resources (RAM, GPU)

### Testing Script

Run the included test script to verify your setup:
```bash
python test_lm_studio.py
```

This will test:
- LM Studio connection
- Available models
- Auto-detection functionality
- Basic presentation generation

## Performance Considerations

### Model Recommendations

| Use Case | Recommended Model | Size | Performance |
|----------|------------------|------|-------------|
| Quick testing | Phi-3 Mini | ~2GB | Fast, good quality |
| Balanced usage | Llama 3.1 8B | ~5GB | Good speed, high quality |
| Best quality | Llama 3.1 70B | ~40GB | Slower, best quality |
| Code-focused | CodeLlama 7B | ~4GB | Good for technical content |

### System Requirements

- **Minimum RAM**: 8GB (for small models)
- **Recommended RAM**: 16GB+ (for 8B models)
- **GPU**: Optional but recommended for faster inference
- **Storage**: 2-50GB depending on model size

## Comparison with Ollama

| Feature | LM Studio | Ollama |
|---------|-----------|--------|
| **Setup** | GUI-based, user-friendly | Command-line, technical |
| **Model Management** | Built-in browser and downloader | Manual model pulling |
| **Interface** | Desktop app with chat UI | Terminal-based |
| **API** | OpenAI-compatible | Custom API |
| **Resource Usage** | Visual monitoring | Command-line monitoring |
| **Model Switching** | GUI model selector | Command-line model switching |

## Advanced Configuration

### Custom Model Parameters

In LM Studio's Local Server tab, you can adjust:
- **Temperature**: Controls creativity (0.1-1.0)
- **Max Tokens**: Maximum response length
- **Context Length**: How much context the model remembers
- **GPU Acceleration**: Enable for faster inference

### Environment Variables

You can also configure via environment variables:
```bash
export LM_STUDIO_URL="http://localhost:1234"
export AI_PROVIDER="lm_studio"
python ppt_maker.py "Your topic"
```

## Integration with Other Tools

### Jupyter Notebooks
```python
from ai_client_manager import AIClientManager

# Create LM Studio client
client = AIClientManager.create_client("lm_studio")

# Generate outline
outline = client.generate_presentation_outline("AI in Education", 5)
print(outline)
```

### Python Scripts
```python
from ppt_generator import PPTGenerator

# Initialize with LM Studio
generator = PPTGenerator(ai_provider="lm_studio")

# Generate presentation
success = generator.generate_presentation(
    prompt="Climate Change Solutions",
    output_file="climate_presentation.pptx",
    num_slides=8
)
```

## Support and Resources

- **LM Studio Website**: [https://lmstudio.ai/](https://lmstudio.ai/)
- **LM Studio Documentation**: [https://lmstudio.ai/docs](https://lmstudio.ai/docs)
- **Model Repository**: [Hugging Face](https://huggingface.co/models)
- **PPT Maker Issues**: [GitHub Issues](https://github.com/studentGarv/PPT-Maker/issues)

## Next Steps

1. **Try the test script**: `python test_lm_studio.py`
2. **Generate your first presentation**: `python ppt_maker.py "Your topic" --provider lm_studio`
3. **Explore the web interface**: `python web_app.py`
4. **Experiment with different models** in LM Studio

---

*LM Studio integration brings the power of local LLMs to PPT Maker with an intuitive, user-friendly interface. Enjoy creating presentations with your own private AI assistant!*
