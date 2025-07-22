#!/usr/bin/env python3
"""
Tests for PPT Maker
"""

import unittest
import os
import tempfile
from unittest.mock import Mock, patch
from ppt_generator import PPTGenerator
from ollama_client import OllamaClient
from pptx_generator import PPTXGenerator


class TestOllamaClient(unittest.TestCase):
    """Test cases for OllamaClient"""
    
    def setUp(self):
        self.client = OllamaClient()
    
    def test_create_fallback_outline(self):
        """Test fallback outline creation"""
        outline = self.client._create_fallback_outline("Test Topic", 4)
        
        self.assertIn('title', outline)
        self.assertIn('slides', outline)
        self.assertEqual(len(outline['slides']), 4)
        self.assertEqual(outline['title'], "Presentation: Test Topic")


class TestPPTXGenerator(unittest.TestCase):
    """Test cases for PPTXGenerator"""
    
    def setUp(self):
        self.generator = PPTXGenerator()
    
    def test_create_presentation(self):
        """Test presentation creation"""
        self.generator.create_presentation("Test Presentation")
        self.assertIsNotNone(self.generator.presentation)
    
    def test_add_title_slide(self):
        """Test adding title slide"""
        self.generator.create_presentation("Test")
        initial_count = len(self.generator.presentation.slides)
        
        self.generator.add_title_slide("Test Title", "Test Subtitle")
        
        self.assertEqual(len(self.generator.presentation.slides), initial_count + 1)
    
    def test_add_content_slide(self):
        """Test adding content slide"""
        self.generator.create_presentation("Test")
        initial_count = len(self.generator.presentation.slides)
        
        content = ["Point 1", "Point 2", "Point 3"]
        self.generator.add_content_slide("Test Content", content)
        
        self.assertEqual(len(self.generator.presentation.slides), initial_count + 1)
    
    def test_save_presentation(self):
        """Test saving presentation"""
        self.generator.create_presentation("Test")
        self.generator.add_title_slide("Test Title")
        
        with tempfile.NamedTemporaryFile(suffix='.pptx', delete=False) as tmp:
            success = self.generator.save_presentation(tmp.name)
            self.assertTrue(success)
            self.assertTrue(os.path.exists(tmp.name))
            
            # Clean up
            os.unlink(tmp.name)


class TestPPTGenerator(unittest.TestCase):
    """Test cases for PPTGenerator"""
    
    def setUp(self):
        self.generator = PPTGenerator()
    
    @patch('ollama_client.ollama.Client')
    def test_generate_presentation_success(self, mock_ollama):
        """Test successful presentation generation"""
        # Mock Ollama response
        mock_response = {
            'message': {
                'content': '''
                {
                    "title": "Test Presentation",
                    "slides": [
                        {
                            "slide_number": 1,
                            "title": "Introduction",
                            "content": ["Point 1", "Point 2"]
                        },
                        {
                            "slide_number": 2,
                            "title": "Conclusion",
                            "content": ["Summary", "Next Steps"]
                        }
                    ]
                }
                '''
            }
        }
        
        mock_client = Mock()
        mock_client.chat.return_value = mock_response
        mock_ollama.return_value = mock_client
        
        # Test generation
        with tempfile.NamedTemporaryFile(suffix='.pptx', delete=False) as tmp:
            success = self.generator.generate_presentation(
                prompt="Test prompt",
                output_file=tmp.name,
                num_slides=2
            )
            
            # Should succeed with mocked response
            self.assertTrue(success)
            self.assertTrue(os.path.exists(tmp.name))
            
            # Clean up
            os.unlink(tmp.name)
    
    def test_invalid_slide_count(self):
        """Test validation of slide count"""
        success = self.generator.generate_presentation(
            prompt="Test",
            num_slides=25  # Too many slides
        )
        self.assertFalse(success)
        
        success = self.generator.generate_presentation(
            prompt="Test",
            num_slides=1  # Too few slides
        )
        self.assertFalse(success)
    
    def test_empty_prompt(self):
        """Test validation of empty prompt"""
        success = self.generator.generate_presentation(prompt="")
        self.assertFalse(success)


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_full_workflow_fallback(self):
        """Test full workflow with fallback (no Ollama connection)"""
        generator = PPTGenerator()
        
        # This should use fallback outline since Ollama likely isn't available in tests
        with tempfile.NamedTemporaryFile(suffix='.pptx', delete=False) as tmp:
            # Mock the Ollama client to return fallback
            with patch.object(generator.ollama_client, 'generate_presentation_outline') as mock_outline:
                mock_outline.return_value = generator.ollama_client._create_fallback_outline("Test", 4)
                
                success = generator.generate_presentation(
                    prompt="Test integration",
                    output_file=tmp.name,
                    num_slides=4,
                    enhance_content=False  # Skip enhancement to avoid Ollama calls
                )
                
                self.assertTrue(success)
                self.assertTrue(os.path.exists(tmp.name))
                
                # Check file size (should be > 0)
                self.assertGreater(os.path.getsize(tmp.name), 0)
                
                # Clean up
                os.unlink(tmp.name)


def run_tests():
    """Run all tests"""
    unittest.main(verbosity=2)


if __name__ == "__main__":
    run_tests()
