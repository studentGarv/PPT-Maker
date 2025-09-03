# Configuration settings for PPT Maker
import datetime

# Ollama settings
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "gpt-oss:20b"

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