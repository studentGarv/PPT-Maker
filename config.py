# Configuration settings for PPT Maker
import datetime

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
        "default_model": "gpt-oss-20b",  # GPT OSS 20B as default
        "timeout": {
            "connection": 10,      # Connection test timeout
            "outline": 300,        # Outline generation timeout (5 minutes)
            "enhancement": 120     # Content enhancement timeout (2 minutes)
        }
    }
}

# Default AI provider (can be overridden)
DEFAULT_AI_PROVIDER = "ollama"

# Legacy settings for backward compatibility
OLLAMA_BASE_URL = AI_PROVIDERS["ollama"]["base_url"]
DEFAULT_MODEL = AI_PROVIDERS["ollama"]["default_model"]

# Presentation settings
DEFAULT_SLIDES_COUNT = 8
MAX_SLIDES_COUNT = 20
MIN_SLIDES_COUNT = 2

# Slide content limits
MAX_TITLE_LENGTH = 100
MAX_CONTENT_LENGTH = 500
MAX_BULLET_POINTS = 6

# Template settings
SLIDE_WIDTH = 10
SLIDE_HEIGHT = 7.5

# Output settings
def get_default_output_file():
    """Generate a default output filename with current timestamp"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"presentation_{timestamp}.pptx"

def get_timestamped_filename(base_name: str = "presentation", extension: str = ".pptx"):
    """Generate a timestamped filename"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}{extension}"

def get_improved_filename(original_path: str):
    """Generate an improved filename based on original file"""
    import os
    base_name = os.path.splitext(os.path.basename(original_path))[0]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_improved_{timestamp}.pptx"

DEFAULT_OUTPUT_FILE = get_default_output_file()