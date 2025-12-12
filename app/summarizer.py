"""
Document Summarizer using T5 model
Handles text summarization and contextual binding
"""

import os
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import logging

logger = logging.getLogger(__name__)

class DocumentSummarizer:
    """Summarizes documents using a fine-tuned T5 model"""
    
    def __init__(self, model_path, tokenizer_path, device="cpu", config=None):
        """
        Initialize the summarizer with model and tokenizer
        
        Args:
            model_path: Path to the model file
            tokenizer_path: Path to the tokenizer files
            device: Device to use ('cpu' or 'cuda')
            config: Configuration object with model parameters
        """
        self.device = device
        self.config = config
        self.model = None
        self.tokenizer = None
        
        try:
            logger.info(f"Loading model from {model_path}...")
            self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                tokenizer_path,
                device_map=device if device != "cpu" else None
            )
            self.model.to(device)
            self.model.eval()
            logger.info("Model loaded successfully!")
        except Exception as e:
            logger.warning(f"Could not load custom model: {e}. Loading T5-base...")
            self._load_default_model()
    
    def _load_default_model(self):
        """Load default T5-base model as fallback"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained("t5-base")
            self.model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")
            self.model.to(self.device)
            self.model.eval()
            logger.info("Default T5-base model loaded successfully!")
        except Exception as e:
            logger.error(f"Failed to load default model: {e}")
            raise
    
    def summarize(self, text, max_length=None, min_length=None, num_beams=None):
        """
        Smart summarizer:
        - auto-adjusts summary length based on input size
        - prevents premature stopping
        - avoids repetition
        - ensures output is complete
        """
        if not text or not text.strip():
            return {"summary": "", "error": "Empty input text"}

        try:
            # ----------------------------------------
            # 1. Measure input length
            # ----------------------------------------
            input_len = len(self.tokenizer.encode(text))

            # Auto length selection (optimized)
            if input_len < 80:
                out_len = 60
            elif input_len < 150:
                out_len = 120
            elif input_len < 250:
                out_len = 180
            elif input_len < 350:
                out_len = 250
            else:
                out_len = 350  # Cap to avoid GPU overload

            # Minimum length (very important)
            min_len = max(30, out_len // 3)

            # ----------------------------------------
            # 2. Tokenize Input
            # ----------------------------------------
            inputs = self.tokenizer(
                "summarize: " + text,
                return_tensors="pt",
                truncation=True,
                max_length=512   # T5-base limit
            ).to(self.device)

            # ----------------------------------------
            # 3. Generate Summary with Safe Settings
            # ----------------------------------------
            with torch.no_grad():
                summary_ids = self.model.generate(
                    **inputs,
                    max_new_tokens=out_len,
                    min_length=min_len,
                    num_beams=num_beams or 4,                 # 4 beams is more stable than 6
                    no_repeat_ngram_size=2,      # safer, less cutting
                    repetition_penalty=1.3,      # balanced; avoids early cutoff
                    length_penalty=0.8,          # allows longer output
                    early_stopping=False,
                )

            # ----------------------------------------
            # 4. Decode Output
            # ----------------------------------------
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

            return {
                "summary": summary,
                "original_length": len(text.split()),
                "summary_length": len(summary.split()),
                "compression_ratio": round(len(summary.split()) / (len(text.split()) + 1e-6), 2)
            }

        except Exception as e:
            logger.error(f"Error during summarization: {e}")
            return {"summary": "", "error": str(e)}
    
    def summarize_with_context(self, text, context=None, max_length=None):
        """
        Summarize text with optional context binding
        
        Args:
            text: Main text to summarize
            context: Additional context to consider
            max_length: Maximum summary length
        
        Returns:
            dict: Contains summary and context information
        """
        result = {"context": context}
        
        try:
            if context:
                # Prepend context to text for contextual summarization
                combined_text = f"Context: {context}\n\nDocument: {text}"
            else:
                combined_text = text
            
            summary_result = self.summarize(combined_text, max_length=max_length)
            result.update(summary_result)
            
            return result
        
        except Exception as e:
            logger.error(f"Error during contextual summarization: {e}")
            result["error"] = str(e)
            return result
    
    def extract_key_sentences(self, text, num_sentences=3):
        """
        Extract key sentences from text using summarization
        
        Args:
            text: Input text
            num_sentences: Number of key sentences to extract
        
        Returns:
            list: Key sentences
        """
        try:
            # Use extractive approach: get summary and split into sentences
            result = self.summarize(text, max_length=150)
            summary = result.get("summary", "")
            
            sentences = [s.strip() for s in summary.split('.') if s.strip()]
            return sentences[:num_sentences]
        
        except Exception as e:
            logger.error(f"Error extracting key sentences: {e}")
            return []
