#!/usr/bin/env python3
"""
PPT Maker - Command Line Interface
Generate PowerPoint presentations from text prompts using AI (Ollama or LM Studio)
"""

import argparse
import sys
import os
from ppt_generator import PPTGenerator
from ai_client_manager import AIClientManager
from config import DEFAULT_SLIDES_COUNT, MAX_SLIDES_COUNT, MIN_SLIDES_COUNT, DEFAULT_MODEL, DEFAULT_AI_PROVIDER, AI_PROVIDERS, get_timestamped_filename


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
        help=f"AI model to use (default: {DEFAULT_MODEL} for Ollama, auto-selected for LM Studio)"
    )
    
    parser.add_argument(
        "--provider",
        choices=list(AI_PROVIDERS.keys()),
        default=DEFAULT_AI_PROVIDER,
        help=f"AI provider to use: {', '.join(AI_PROVIDERS.keys())} (default: {DEFAULT_AI_PROVIDER})"
    )
    
    parser.add_argument(
        "--base-url",
        help="Custom base URL for AI service (overrides default)"
    )
    
    parser.add_argument(
        "--ollama-url",
        help="Ollama server URL (deprecated, use --base-url instead)"
    )
    
    parser.add_argument(
        "--no-enhance",
        action="store_true",
        help="Skip content enhancement (faster but less detailed)"
    )
    
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List all available models from current AI provider"
    )
    
    parser.add_argument(
        "--test-connection",
        action="store_true",
        help="Test connection to AI service and list available models"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Handle backward compatibility for --ollama-url
    base_url = args.base_url or args.ollama_url
    
    # Create generator with appropriate AI provider
    try:
        generator = PPTGenerator(
            model=args.model, 
            ai_provider=args.provider,
            base_url=base_url
        )
    except Exception as e:
        print(f"❌ Error initializing generator: {e}")
        return 1
    
    # Test connection if requested
    if args.test_connection:
        print(f"Testing connection to {args.provider.upper()}...")
        if generator.test_connection():
            print(f"✅ Connected to {args.provider.upper()} successfully!")
            models = generator.list_available_models()
            if models:
                print(f"Available models: {', '.join(models)}")
            else:
                print("No models found or error listing models")
        else:
            print(f"❌ Cannot connect to {args.provider.upper()}")
            if args.provider == 'ollama':
                print("Make sure Ollama is running with: ollama serve")
            elif args.provider == 'lm_studio':
                print("Make sure LM Studio is running with a model loaded")
            return 1
        return 0
    
    # List models if requested
    if args.list_models:
        print(f"Listing available models from {args.provider.upper()}...")
        models = generator.list_available_models()
        if models:
            print("Available models:")
            for model in models:
                prefix = "* " if model == DEFAULT_MODEL else "  "
                print(f"{prefix}{model}")
            print(f"\nDefault model: {DEFAULT_MODEL}")
        else:
            print(f"No models found or error connecting to {args.provider.upper()}")
            if args.provider == 'ollama':
                print("Make sure Ollama is running with: ollama serve")
            elif args.provider == 'lm_studio':
                print("Make sure LM Studio is running with a model loaded")
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
    
    # Test AI service connection first
    if not generator.test_connection():
        print(f"❌ Cannot connect to {args.provider.upper()}. Please make sure your AI service is running.")
        if args.provider == 'ollama':
            print("Start Ollama with: ollama serve")
        elif args.provider == 'lm_studio':
            print("Start LM Studio and load a model")
        print("Or use --test-connection to test your setup")
        return 1
    
    if args.verbose:
        print(f"Using model: {args.model}")
        print(f"AI Provider: {args.provider}")
        print(f"Base URL: {base_url or 'default'}")
        print(f"Slides: {args.slides}")
        
        # Set default output filename if not provided
        if not args.output:
            args.output = get_timestamped_filename("presentation")
        
        print(f"Output: {args.output}")
        print(f"Enhance content: {not args.no_enhance}")
        print()
    else:
        # Set default output filename if not provided
        if not args.output:
            args.output = get_timestamped_filename("presentation")
    
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
