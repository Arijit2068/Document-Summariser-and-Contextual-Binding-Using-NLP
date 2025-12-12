import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from ui.ewb_app import initialize_app

class TestAppInitialization(unittest.TestCase):

    @patch('ui.ewb_app.DocumentSummarizer')
    @patch('ui.ewb_app.DocumentChatbot')
    @patch('ui.ewb_app.HistoryManager')
    def test_summarizer_initialization_failure(self, MockHistoryManager, MockDocumentChatbot, MockDocumentSummarizer):
        # Force an exception when the summarizer is initialized
        MockDocumentSummarizer.side_effect = Exception("Test summarizer initialization error")

        # Attempt to initialize the app
        app = initialize_app()

        # Check that the summarizer is None
        self.assertIsNone(app.summarizer)

if __name__ == '__main__':
    unittest.main()