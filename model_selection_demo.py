#!/usr/bin/env python3
"""
LM Studio Model Selection Demo
Shows how model selection works with LM Studio integration
"""

from lm_studio_client import LMStudioClient
from ai_client_manager import AIClientManager
import sys


def demonstrate_model_selection():
    """Demonstrate model selection capabilities"""
    print("🎯 LM Studio Model Selection Demo")
    print("=" * 50)
    
    try:
        client = LMStudioClient()
        
        if not client.test_connection():
            print("❌ LM Studio not available")
            print("   Make sure LM Studio is running with a model loaded")
            return
        
        print("✅ LM Studio connection successful!")
        print()
        
        # 1. Show all available models
        print("📋 Available Models:")
        models = client.get_available_models()
        
        if not models:
            print("   No models detected")
            return
            
        for i, model in enumerate(models, 1):
            model_type = "🧠 Text Generation" if 'embedding' not in model.lower() else "🔍 Embedding"
            print(f"   {i}. {model} ({model_type})")
        
        print()
        
        # 2. Show best model selection
        print("🤖 Auto-Selected Best Model:")
        best_model = client.select_best_model()
        print(f"   {best_model}")
        print()
        
        # 3. Show currently loaded model (if detectable)
        print("🔄 Currently Active Model:")
        try:
            loaded_model = client.get_loaded_model()
            print(f"   {loaded_model}")
        except Exception as e:
            print(f"   Could not detect: {e}")
        print()
        
        # 4. Demonstrate model usage
        print("🧪 Testing Model Selection:")
        
        # Test with auto-selected model
        auto_client = LMStudioClient()  # Uses auto-selection
        model_used = auto_client.get_model_to_use()
        print(f"   Auto-selection will use: {model_used}")
        
        # Test with specific model (first text model)
        text_models = [m for m in models if 'embedding' not in m.lower()]
        if text_models:
            specific_client = LMStudioClient(model=text_models[0])
            specific_model = specific_client.get_model_to_use()
            print(f"   Explicit selection: {specific_model}")
        
        print()
        
        # 5. Show model preferences
        print("🎖️ Model Selection Preferences (in order):")
        preferences = [
            "1. Llama models (llama-*)",
            "2. Instruction-tuned models (*instruct*)",
            "3. Chat models (*chat*)",
            "4. Mistral models (mistral-*)",
            "5. Qwen models (qwen-*)",
            "6. GPT-style models (gpt-*)",
            "7. Any other text generation model"
        ]
        
        for pref in preferences:
            print(f"   {pref}")
        
        print()
        print("💡 Models with 'embedding' in the name are excluded from text generation")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def show_model_recommendations():
    """Show model recommendations for different use cases"""
    print("\n🎯 Model Recommendations for PPT Generation")
    print("=" * 50)
    
    recommendations = [
        {
            "category": "🚀 Best Overall",
            "models": ["meta-llama/Llama-3.1-8B-Instruct", "mistralai/Mistral-7B-Instruct-v0.3"],
            "description": "Balanced performance, good for most presentations"
        },
        {
            "category": "⚡ Fast & Efficient", 
            "models": ["microsoft/Phi-3-mini-4k-instruct", "TinyLlama/TinyLlama-1.1B-Chat"],
            "description": "Quick generation, suitable for simple presentations"
        },
        {
            "category": "🎨 Creative Content",
            "models": ["meta-llama/Llama-3.1-70B-Instruct", "anthropic/claude-3-haiku"],
            "description": "High-quality, creative content generation (requires more resources)"
        },
        {
            "category": "💼 Business/Technical",
            "models": ["Qwen/Qwen2.5-7B-Instruct", "codellama/CodeLlama-7b-Instruct"],
            "description": "Good for technical and business presentations"
        }
    ]
    
    for rec in recommendations:
        print(f"\n{rec['category']}")
        print(f"   Description: {rec['description']}")
        print("   Recommended models:")
        for model in rec['models']:
            print(f"     • {model}")


def interactive_model_test():
    """Interactive model testing"""
    print("\n🧪 Interactive Model Test")
    print("=" * 30)
    
    try:
        client = LMStudioClient()
        models = client.get_available_models()
        
        if not models:
            print("No models available for testing")
            return
        
        print("Available models for testing:")
        text_models = [m for m in models if 'embedding' not in m.lower()]
        
        for i, model in enumerate(text_models, 1):
            print(f"  {i}. {model}")
        
        try:
            choice = input(f"\nSelect model (1-{len(text_models)}) or press Enter for auto-selection: ").strip()
            
            if choice:
                selected_model = text_models[int(choice) - 1]
                test_client = LMStudioClient(model=selected_model)
                print(f"Testing with: {selected_model}")
            else:
                test_client = LMStudioClient()
                print(f"Testing with auto-selected model: {test_client.get_model_to_use()}")
            
            print("\nGenerating test outline...")
            outline = test_client.generate_presentation_outline("Test presentation about renewable energy", 3)
            
            if outline and 'slides' in outline:
                print("✅ Success! Generated outline:")
                print(f"   Title: {outline.get('title', 'No title')}")
                print(f"   Slides: {len(outline['slides'])}")
            else:
                print("❌ Failed to generate outline")
                
        except (ValueError, IndexError):
            print("Invalid selection")
        except KeyboardInterrupt:
            print("\nTest cancelled")
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--recommendations":
            show_model_recommendations()
        elif sys.argv[1] == "--interactive":
            interactive_model_test()
        elif sys.argv[1] == "--help":
            print("Usage:")
            print("  python model_selection_demo.py              # Basic demo")
            print("  python model_selection_demo.py --recommendations # Show model recommendations")
            print("  python model_selection_demo.py --interactive     # Interactive testing")
            print("  python model_selection_demo.py --help           # This help")
        else:
            print("Unknown option. Use --help for usage.")
    else:
        demonstrate_model_selection()
        
        # Ask if user wants to see more
        try:
            response = input("\n❓ Show model recommendations? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                show_model_recommendations()
                
            response = input("\n❓ Try interactive testing? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                interactive_model_test()
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
