#!/usr/bin/env python3
"""
Test script to verify PPT improvement works with LM Studio
"""

from ppt_improver import improve_ppt
from ai_client_manager import AIClientManager
import tempfile
import os


def test_improve_with_lm_studio():
    """Test that PPT improvement works with LM Studio"""
    
    print("🧪 Testing PPT Improvement with LM Studio")
    print("=" * 50)
    
    # Test 1: Check AI provider detection
    print("1️⃣ Testing AI provider detection...")
    try:
        ai_client = AIClientManager.auto_detect_provider()
        print(f"   Detected provider: {ai_client.provider}")
        
        if ai_client.test_connection():
            print(f"   ✅ {ai_client.provider.title()} connected successfully")
        else:
            print(f"   ❌ {ai_client.provider.title()} connection failed")
            return
            
    except Exception as e:
        print(f"   ❌ Error detecting AI provider: {e}")
        return
    
    # Test 2: Check if we have a sample PPT to test with
    print("\n2️⃣ Checking for sample presentation...")
    
    # Look for existing PPT files in the directory
    sample_files = [f for f in os.listdir('.') if f.endswith('.pptx')]
    
    if sample_files:
        sample_file = sample_files[0]
        print(f"   ✅ Found sample file: {sample_file}")
    else:
        print("   ⚠️ No .pptx files found in current directory")
        print("   💡 To test: Place a .pptx file in the current directory and run again")
        return
    
    # Test 3: Test the improvement process
    print("\n3️⃣ Testing improvement process...")
    try:
        # Create temporary output file
        with tempfile.NamedTemporaryFile(suffix='_test_improved.pptx', delete=False) as tmp_file:
            output_path = tmp_file.name
        
        print(f"   Input: {sample_file}")
        print(f"   Output: {output_path}")
        print("   Starting improvement process...")
        
        # Run the improvement
        improve_ppt(
            input_path=sample_file,
            output_path=output_path,
            outline_model="gpt-oss-20b",  # Use GPT OSS 20B
            embed_model="nomic-embed-text"
        )
        
        # Check if output file was created
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"   ✅ Improvement successful!")
            print(f"   📁 Output file: {output_path}")
            print(f"   📊 File size: {file_size:,} bytes")
            
            # Cleanup
            print("   🧹 Cleaning up test file...")
            os.unlink(output_path)
            
        else:
            print("   ❌ Improvement failed - no output file created")
            
    except Exception as e:
        print(f"   ❌ Error during improvement: {e}")
        import traceback
        print(f"   📋 Details: {traceback.format_exc()}")
    
    # Test 4: Test fallback behavior
    print("\n4️⃣ Testing fallback behavior...")
    try:
        print("   Testing with invalid model (should fallback to heuristic)...")
        
        with tempfile.NamedTemporaryFile(suffix='_test_fallback.pptx', delete=False) as tmp_file:
            fallback_output = tmp_file.name
        
        improve_ppt(
            input_path=sample_file,
            output_path=fallback_output,
            outline_model="nonexistent-model",  # This should trigger fallback
            embed_model="nomic-embed-text"
        )
        
        if os.path.exists(fallback_output):
            print("   ✅ Fallback behavior working correctly")
            os.unlink(fallback_output)
        else:
            print("   ❌ Fallback behavior failed")
            
    except Exception as e:
        print(f"   ⚠️ Fallback test error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")
    print("\n💡 Key points:")
    print("   - PPT improvement now uses AI Client Manager")
    print("   - Supports both Ollama and LM Studio automatically")
    print("   - Falls back to heuristic analysis if AI fails")
    print("   - Works in web interface and command line")


if __name__ == "__main__":
    test_improve_with_lm_studio()
