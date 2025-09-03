#!/usr/bin/env python3
"""
PPT Maker - Command Line Interface
Generate PowerPoint presentations from text prompts using Ollama and python-pptx
"""

import argparse
import sys
import os
from ppt_generator import PPTGenerator
from config import DEFAULT_SLIDES_COUNT, MAX_SLIDES_COUNT, MIN_SLIDES_COUNT, DEFAULT_MODEL, get_default_output_file


def main():
    parser = argparse.ArgumentParser(
        description="Generate PowerPoint presentations from text prompts using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  %(prog)s "Create a presentation about artificial intelligence"
  %(prog)s "Business plan for a tech startup" --output "startup.pptx" --slides 10
  %(prog)s "Python programming basics" --model "mistral" --no-enhance
  %(prog)s --list-models
  %(prog)s --test-connection

Current default model: {DEFAULT_MODEL}
        """
    )
    
    parser.add_argument(
        "prompt",
        nargs='?',
        help="Text prompt describing the presentation to generate"
    )
    
    parser.add_argument(
        "-o", "--output",
        default=None,  # Will be set to timestamped name if not provided
        help="Output filename (default: auto-generated with timestamp)"
    )
    
    parser.add_argument(
        "-s", "--slides",
        type=int,
        default=DEFAULT_SLIDES_COUNT,
        help=f"Number of slides to generate (default: {DEFAULT_SLIDES_COUNT}, range: {MIN_SLIDES_COUNT}-{MAX_SLIDES_COUNT})"
    )
    
    parser.add_argument(
        "-m", "--model",
        default=DEFAULT_MODEL,
        help=f"Ollama model to use (default: {DEFAULT_MODEL})"
    )
    
    parser.add_argument(
        "--ollama-url",
        default="http://localhost:11434",
        help="Ollama server URL (default: http://localhost:11434)"
    )
    
    parser.add_argument(
        "--no-enhance",
        action="store_true",
        help="Skip content enhancement (faster but less detailed)"
    )
    
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List all available Ollama models"
    )
    
    parser.add_argument(
        "--test-connection",
        action="store_true",
        help="Test connection to Ollama and list available models"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Create generator
    try:
        generator = PPTGenerator(model=args.model, ollama_url=args.ollama_url)
    except Exception as e:
        print(f"❌ Error initializing generator: {e}")
        return 1
    
    # Test connection if requested
    if args.test_connection:
        print("Testing connection to Ollama...")
        if generator.test_ollama_connection():
            print("✅ Connected to Ollama successfully!")
            models = generator.list_available_models()
            if models:
                print(f"Available models: {', '.join(models)}")
            else:
                print("No models found or error listing models")
        else:
            print("❌ Cannot connect to Ollama")
            print("Make sure Ollama is running with: ollama serve")
            return 1
        return 0
    
    # List models if requested
    if args.list_models:
        print("Listing available Ollama models...")
        models = generator.list_available_models()
        if models:
            print("Available models:")
            for model in models:
                prefix = "* " if model == DEFAULT_MODEL else "  "
                print(f"{prefix}{model}")
            print(f"\nDefault model: {DEFAULT_MODEL}")
        else:
            print("No models found or error connecting to Ollama")
            print("Make sure Ollama is running with: ollama serve")
            return 1
        return 0
    
    # Validate prompt is provided when not testing connection or listing models
    if not args.prompt and not args.test_connection and not args.list_models:
        print("❌ Error: Prompt is required")
        parser.print_help()
        return 1
    
    # Validate arguments
    if not args.prompt.strip():
        print("❌ Error: Prompt cannot be empty")
        return 1
    
    if args.slides < MIN_SLIDES_COUNT or args.slides > MAX_SLIDES_COUNT:
        print(f"❌ Error: Number of slides must be between {MIN_SLIDES_COUNT} and {MAX_SLIDES_COUNT}")
        return 1
    
    # Test Ollama connection first
    if not generator.test_ollama_connection():
        print("❌ Cannot connect to Ollama. Please make sure Ollama is running.")
        print("Start Ollama with: ollama serve")
        print("Or use --test-connection to test your setup")
        return 1
    
    if args.verbose:
        print(f"Using model: {args.model}")
        print(f"Ollama URL: {args.ollama_url}")
        print(f"Slides: {args.slides}")
        
        # Set default output filename if not provided
        if not args.output:
            args.output = get_default_output_file()
        
        print(f"Output: {args.output}")
        print(f"Enhance content: {not args.no_enhance}")
        print()
    else:
        # Set default output filename if not provided
        if not args.output:
            args.output = get_default_output_file()
    
    # Generate presentation
    print(f"🚀 Generating presentation: '{args.prompt}'")
    
    success = generator.generate_presentation(
        prompt=args.prompt,
        output_file=args.output,
        num_slides=args.slides,
        enhance_content=not args.no_enhance
    )
    
    if success:
        print(f"\n🎉 Presentation created successfully!")
        print(f"📁 File: {os.path.abspath(args.output)}")
        print(f"📊 Slides: {args.slides}")
        return 0
    else:
        print("\n❌ Failed to create presentation")
        return 1


if __name__ == "__main__":
    sys.exit(main())
