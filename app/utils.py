"""
Utility functions for text processing and data management
"""

import json
import os
import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class TextProcessor:
    """Handle text preprocessing and cleaning"""
    
    @staticmethod
    def clean_text(text):
        """
        Clean and normalize text
        
        Args:
            text: Input text
        
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-\']', '', text)
        
        # Trim
        text = text.strip()
        
        return text
    
    @staticmethod
    def split_sentences(text):
        """
        Split text into sentences
        
        Args:
            text: Input text
        
        Returns:
            list: List of sentences
        """
        # Simple sentence splitter using regex
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    @staticmethod
    def split_paragraphs(text):
        """
        Split text into paragraphs
        
        Args:
            text: Input text
        
        Returns:
            list: List of paragraphs
        """
        paragraphs = text.split('\n\n')
        return [p.strip() for p in paragraphs if p.strip()]
    
    @staticmethod
    def get_word_count(text):
        """
        Get word count of text
        
        Args:
            text: Input text
        
        Returns:
            int: Word count
        """
        return len(text.split())
    
    @staticmethod
    def get_reading_time(text, wpm=200):
        """
        Estimate reading time
        
        Args:
            text: Input text
            wpm: Words per minute (default 200)
        
        Returns:
            int: Estimated reading time in minutes
        """
        word_count = TextProcessor.get_word_count(text)
        return max(1, word_count // wpm)


class ContextBinder:
    """Handle contextual binding and relationship extraction"""
    
    @staticmethod
    def extract_keywords(text, num_keywords=5):
        """
        Extract keywords from text (simple frequency-based)
        
        Args:
            text: Input text
            num_keywords: Number of keywords to extract
        
        Returns:
            list: List of keywords
        """
        words = text.lower().split()
        
        # Remove common stopwords
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                    'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'that', 'this', 'what',
                    'which', 'who', 'when', 'where', 'why', 'how'}
        
        words = [w for w in words if w.isalpha() and w not in stopwords and len(w) > 3]
        
        # Simple frequency count
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency
        sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        return [word for word, _ in sorted_keywords[:num_keywords]]
    
    @staticmethod
    def bind_context(text, summary, keywords=None):
        """
        Create context binding information
        
        Args:
            text: Original text
            summary: Generated summary
            keywords: Extracted keywords
        
        Returns:
            dict: Context binding information
        """
        if not keywords:
            keywords = ContextBinder.extract_keywords(text)
        
        return {
            "original_text": text[:200] + "..." if len(text) > 200 else text,
            "summary": summary,
            "keywords": keywords,
            "text_length": len(text.split()),
            "summary_length": len(summary.split()),
            "related_concepts": keywords  # Can be enhanced with NER or other techniques
        }


class HistoryManager:
    """Manage summarization history"""
    
    def __init__(self, history_file):
        """
        Initialize history manager
        
        Args:
            history_file: Path to history JSON file
        """
        self.history_file = history_file
        os.makedirs(os.path.dirname(history_file), exist_ok=True)
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Ensure history file exists"""
        # If file does not exist, create and initialize with empty list
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                json.dump([], f)
            return

        # If file exists but is empty, initialize with empty list
        try:
            if os.path.getsize(self.history_file) == 0:
                with open(self.history_file, 'w') as f:
                    json.dump([], f)
        except OSError:
            # On any filesystem error, attempt to create/overwrite the file
            with open(self.history_file, 'w') as f:
                json.dump([], f)
    
    def add_entry(self, original_text, summary, context=None, keywords=None):
        """
        Add a summarization entry to history
        
        Args:
            original_text: Original text
            summary: Generated summary
            context: Optional context
            keywords: Optional keywords
        
        Returns:
            bool: Success status
        """
        try:
            history = self.get_history()
            
            entry = {
                "timestamp": datetime.now().isoformat(),
                "original_text": original_text[:500],  # Store first 500 chars
                "summary": summary,
                "context": context,
                "keywords": keywords,
                "text_length": len(original_text.split())
            }
            
            history.append(entry)
            
            # Keep only last 100 entries
            if len(history) > 100:
                history = history[-100:]
            
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            return True
        
        except Exception as e:
            logger.error(f"Error adding history entry: {e}")
            return False
    
    def get_history(self, limit=None):
        """
        Get summarization history
        
        Args:
            limit: Maximum number of entries to return
        
        Returns:
            list: History entries
        """
        try:
            with open(self.history_file, 'r') as f:
                content = f.read()
                if not content.strip():
                    # Empty file -> return empty history
                    return []
                history = json.loads(content)

            if limit:
                history = history[-limit:]

            return history

        except json.JSONDecodeError as e:
            logger.error(f"Error reading history (invalid JSON): {e}")
            # Attempt to reinitialize the history file to an empty list
            try:
                with open(self.history_file, 'w') as f:
                    json.dump([], f)
            except Exception as write_err:
                logger.error(f"Failed to reinitialize history file: {write_err}")
            return []

        except Exception as e:
            logger.error(f"Error reading history: {e}")
            return []
    
    def clear_history(self):
        """Clear all history"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump([], f)
            return True
        except Exception as e:
            logger.error(f"Error clearing history: {e}")
            return False
    
    def search_history(self, keyword):
        """
        Search history by keyword
        
        Args:
            keyword: Keyword to search for
        
        Returns:
            list: Matching entries
        """
        history = self.get_history()
        keyword_lower = keyword.lower()
        
        matches = [entry for entry in history 
                  if keyword_lower in entry.get('original_text', '').lower() or
                     keyword_lower in entry.get('summary', '').lower()]
        
        return matches
