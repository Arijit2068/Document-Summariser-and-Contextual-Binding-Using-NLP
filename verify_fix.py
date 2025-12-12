import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Now we can import the modules
from dev_fix import FixedDocumentSummarizer
from app.summarizer import DocumentSummarizer

class TestSummarizerFix(unittest.TestCase):

    @patch('app.summarizer.AutoModelForSeq2SeqLM.from_pretrained')
    @patch('app.summarizer.AutoTokenizer.from_pretrained')
    def test_original_summarizer_fails(self, mock_tokenizer, mock_model):
        """
        Verify that the original DocumentSummarizer fails to load the model
        from a specific file path, which is the incorrect way.
        """
        mock_model.side_effect = OSError("Cannot load model from a file path directly")
        
        with self.assertLogs('app.summarizer', level='WARNING') as cm:
            summarizer = DocumentSummarizer(
                model_path="/path/to/model.safetensors",
                tokenizer_path="/path/to/tokenizer"
            )
            self.assertIn("Could not load custom model", cm.output[0])

    @patch('dev_fix.AutoModelForSeq2SeqLM.from_pretrained')
    @patch('dev_fix.AutoTokenizer.from_pretrained')
    def test_fixed_summarizer_succeeds(self, mock_tokenizer, mock_model):
        """
        Verify that the FixedDocumentSummarizer can successfully load the model
        from the directory containing the .safetensors file.
        """
        mock_model.return_value = MagicMock()
        mock_tokenizer.return_value = MagicMock()
        
        summarizer = FixedDocumentSummarizer(
            model_path="/path/to/model.safetensors",
            tokenizer_path="/path/to/tokenizer"
        )
        
        # Check that the model was loaded from the directory
        mock_model.assert_called_with("/path/to")
        self.assertIsNotNone(summarizer.model)

if __name__ == '__main__':
    unittest.main()