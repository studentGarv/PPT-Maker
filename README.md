# PPT Maker

A Python application that generates PowerPoint presentations from text prompts using Ollama and python-pptx.

## Features

- Generate PowerPoint presentations from natural language prompts
- Uses Ollama for AI-powered content generation
- Creates structured slides with titles and content
- Customizable presentation templates

## Prerequisites

- Python 3.7+
- Ollama installed and running locally
- An Ollama model (e.g., llama3, mistral, etc.)

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure Ollama is installed and running:
```bash
# Install Ollama (if not already installed)
# Visit https://ollama.ai for installation instructions

# Pull a model (example)
ollama pull llama3
ollama serve
```

## Usage

### Command Line Interface
```bash
python ppt_maker.py "Create a presentation about artificial intelligence"
```

## Configuration

You can customize the presentation generation by modifying the configuration in `config.py`:

- Model selection
- Slide templates
- Number of slides
- Content structure

## Command Line Options

```bash
# Basic usage
python ppt_maker.py "Your presentation topic"

# Specify number of slides
python ppt_maker.py "Business strategy" --slides 10

# Custom output file
python ppt_maker.py "Data science overview" --output "data_science.pptx"

# Use different AI model
python ppt_maker.py "Climate change" --model "mistral"

# Fast generation (no content enhancement)
python ppt_maker.py "Quick overview" --no-enhance

# Test Ollama connection
python ppt_maker.py --test-connection

# Verbose output
python ppt_maker.py "Detailed topic" --verbose
```