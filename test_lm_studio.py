#!/usr/bin/env python3
"""
Test script for LM Studio integration
"""

from lm_studio_client import LMStudioClient
from ai_client_manager import AIClientManager
import sys


def test_lm_studio():
    """Test LM Studio connection and functionality"""
    print("🧪 Testing LM Studio Integration")
    print("=" * 50)
    
    # Test 1: Direct LM Studio client
    print("1. Testing direct LM Studio client...")
    try:
        client = LMStudioClient()
        if client.test_connection():
            print("✅ LM Studio connection successful!")
            
            models = client.get_available_models()
            if models:
                print(f"   Available models: {', '.join(models)}")
            else:
                print("   No models detected (this is normal if no model is loaded)")
        else:
            print("❌ LM Studio connection failed")
            print("   Make sure LM Studio is running and has a model loaded")
            
    except Exception as e:
        print(f"❌ LM Studio test failed: {e}")
    
    print()
    
    # Test 2: AI Client Manager auto-detection
    print("2. Testing AI Client Manager auto-detection...")
    try:
        manager = AIClientManager.auto_detect_provider()
        print(f"   Detected provider: {manager.provider}")
        print(f"   Connection status: {'✅ Connected' if manager.test_connection() else '❌ Failed'}")
        
        models = manager.get_available_models()
        if models:
            print(f"   Available models: {', '.join(models[:3])}{'...' if len(models) > 3 else ''}")
        
    except Exception as e:
        print(f"❌ Auto-detection failed: {e}")
    
    print()
    
    # Test 3: Create a simple presentation
    print("3. Testing presentation generation...")
    try:
        manager = AIClientManager.auto_detect_provider()
        if manager.test_connection():
            print("   Generating test outline...")
            outline = manager.generate_presentation_outline("Test presentation about AI", 3)
            
            if outline and 'slides' in outline:
                print(f"✅ Generated outline with {len(outline['slides'])} slides")
                print(f"   Title: {outline.get('title', 'No title')}")
                if outline['slides']:
                    print(f"   First slide: {outline['slides'][0].get('title', 'No title')}")
            else:
                print("❌ Failed to generate outline")
        else:
            print("❌ No AI service available for testing")
            
    except Exception as e:
        print(f"❌ Presentation generation test failed: {e}")


def print_usage():
    """Print usage instructions"""
    print()
    print("📋 LM Studio Setup Instructions:")
    print("=" * 50)
    print("1. Download and install LM Studio from: https://lmstudio.ai/")
    print("2. Start LM Studio application")
    print("3. Download a model (recommended: Llama 3.1 8B or similar)")
    print("4. Load the model in LM Studio's Chat tab")
    print("5. Go to Local Server tab and click 'Start Server'")
    print("6. Ensure server is running on default port 1234")
    print("7. Run this test script again")
    print()
    print("💡 Alternative: Use with Ollama")
    print("   1. Install Ollama: https://ollama.com/")
    print("   2. Run: ollama serve")
    print("   3. Run: ollama run gpt-oss:20b")


if __name__ == "__main__":
    test_lm_studio()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print_usage()
    else:
        print()
        print("💡 Run with --help to see setup instructions")
