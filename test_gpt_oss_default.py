#!/usr/bin/env python3
"""
Test script to verify GPT OSS 20B is set as default for LM Studio
"""

from lm_studio_client import LMStudioClient
from ai_client_manager import AIClientManager
from config import AI_PROVIDERS
import json


def test_gpt_oss_default():
    """Test that GPT OSS 20B is properly configured as default"""
    
    print("🧪 Testing GPT OSS 20B Default Configuration")
    print("=" * 50)
    
    # Test 1: Check config
    print("1️⃣ Checking config.py settings...")
    lm_studio_config = AI_PROVIDERS.get("lm_studio", {})
    default_model = lm_studio_config.get("default_model")
    print(f"   Default LM Studio model in config: {default_model}")
    
    if default_model == "gpt-oss-20b":
        print("   ✅ Config correctly set to gpt-oss-20b")
    else:
        print(f"   ❌ Config issue: expected 'gpt-oss-20b', got '{default_model}'")
    
    # Test 2: Check LM Studio client initialization
    print("\n2️⃣ Testing LM Studio client initialization...")
    try:
        client = LMStudioClient()
        print(f"   Client default model: {client.model}")
        
        if client.model == "gpt-oss-20b":
            print("   ✅ LM Studio client correctly initialized with gpt-oss-20b")
        else:
            print(f"   ❌ Client issue: expected 'gpt-oss-20b', got '{client.model}'")
    except Exception as e:
        print(f"   ❌ Error initializing client: {e}")
    
    # Test 3: Check connection and model detection
    print("\n3️⃣ Testing LM Studio connection and model detection...")
    try:
        if client.test_connection():
            print("   ✅ Connected to LM Studio successfully")
            
            # Get available models
            models = client.get_available_models()
            print(f"   Available models: {models}")
            
            # Test model selection
            selected_model = client.select_best_model()
            print(f"   Auto-selected model: {selected_model}")
            
            # Check if GPT OSS is available and selected
            gpt_oss_models = [m for m in models if 'gpt-oss' in m.lower()]
            if gpt_oss_models:
                print(f"   ✅ Found GPT OSS models: {gpt_oss_models}")
                if 'gpt-oss' in selected_model.lower():
                    print("   ✅ GPT OSS model automatically selected")
                else:
                    print(f"   ⚠️ GPT OSS available but not selected: {selected_model}")
            else:
                print("   ⚠️ No GPT OSS models found in LM Studio")
                
        else:
            print("   ❌ Cannot connect to LM Studio")
            print("   💡 Make sure LM Studio is running and has a model loaded")
            
    except Exception as e:
        print(f"   ❌ Error testing connection: {e}")
    
    # Test 4: Check AI Client Manager auto-detection
    print("\n4️⃣ Testing AI Client Manager with LM Studio...")
    try:
        ai_client = AIClientManager.auto_detect_provider()
        print(f"   Detected provider: {ai_client.provider}")
        
        if ai_client.provider == "lm_studio":
            print("   ✅ LM Studio correctly detected as primary provider")
            model_in_use = ai_client.client.get_model_to_use()
            print(f"   Model in use: {model_in_use}")
            
            if 'gpt-oss' in model_in_use.lower():
                print("   ✅ GPT OSS model is being used")
            else:
                print(f"   ⚠️ Different model in use: {model_in_use}")
        else:
            print(f"   ⚠️ Different provider detected: {ai_client.provider}")
            
    except Exception as e:
        print(f"   ❌ Error with AI Client Manager: {e}")
    
    # Test 5: Quick generation test
    print("\n5️⃣ Testing quick outline generation...")
    try:
        if client.test_connection():
            print("   Generating test outline...")
            outline = client.generate_presentation_outline("Test AI presentation", 3)
            
            if outline and 'title' in outline:
                print("   ✅ Successfully generated outline")
                print(f"   Title: {outline.get('title', 'N/A')}")
                print(f"   Slides: {len(outline.get('slides', []))}")
            else:
                print("   ❌ Failed to generate outline")
        else:
            print("   ⏭️ Skipping generation test (no connection)")
            
    except Exception as e:
        print(f"   ❌ Error in generation test: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")
    print("\n💡 If you see issues:")
    print("   - Make sure LM Studio is running")
    print("   - Ensure GPT OSS 20B model is loaded in LM Studio")
    print("   - Check that the model name matches exactly")


if __name__ == "__main__":
    test_gpt_oss_default()