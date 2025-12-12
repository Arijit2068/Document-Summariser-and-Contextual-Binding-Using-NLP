import os
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import logging
from app.summarizer import DocumentSummarizer

logger = logging.getLogger(__name__)

class FixedDocumentSummarizer(DocumentSummarizer):
    """
    A fixed version of the DocumentSummarizer that correctly loads the local model.
    """
    def __init__(self, model_path, tokenizer_path, device="cpu", config=None):
        """
        Initialize the summarizer with model and tokenizer
        
        Args:
            model_path: Path to the model file or directory
            tokenizer_path: Path to the tokenizer files
            device: Device to use ('cpu' or 'cuda')
            config: Configuration object with model parameters
        """
        self.device = device
        self.config = config
        self.model = None
        self.tokenizer = None
        
        try:
            logger.info(f"Loading tokenizer from {tokenizer_path}...")
            self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
            
            logger.info(f"Loading model from {model_path}...")
            # This is the key fix: loading the model from the directory containing the .safetensors file
            self.model = AutoModelForSeq2SeqLM.from_pretrained(os.path.dirname(model_path))
            
            self.model.to(self.device)
            self.model.eval()
            logger.info("Model loaded successfully!")
        except Exception as e:
            logger.warning(f"Could not load custom model: {e}. Loading T5-base...")
            self._load_default_model()