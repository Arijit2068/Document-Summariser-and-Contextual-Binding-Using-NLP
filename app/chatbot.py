"""
Chatbot for contextual question answering based on summarized documents
"""

import logging
import torch
from app.summarizer import DocumentSummarizer
from app.utils import TextProcessor, ContextBinder

logger = logging.getLogger(__name__)

class DocumentChatbot:
    """Chatbot that answers questions based on document context"""

    def __init__(self, summarizer):
        """
        Initialize chatbot with a summarizer

        Args:
            summarizer: DocumentSummarizer instance
        """
        self.summarizer = summarizer
        self.document_context = None
        self.summary = None
        self.keywords = []

    def load_document(self, document_text):
        """
        Load a document for context

        Args:
            document_text: The document to analyze

        Returns:
            dict: Document analysis results
        """
        try:
            self.document_context = document_text

            # Generate summary
            result = self.summarizer.summarize(document_text)
            self.summary = result.get('summary', '')

            # Extract keywords
            self.keywords = ContextBinder.extract_keywords(document_text, num_keywords=10)

            return {
                "success": True,
                "message": "Document loaded successfully",
                "word_count": TextProcessor.get_word_count(document_text),
                "reading_time": TextProcessor.get_reading_time(document_text),
                "summary": self.summary,
                "keywords": self.keywords
            }

        except Exception as e:
            logger.error(f"Error loading document: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def answer_question(self, question):
        """
        Answer a question based on loaded document context

        Args:
            question: User's question

        Returns:
            dict: Answer and related information
        """
        if not self.document_context:
            return {
                "success": False,
                "error": "No document loaded. Please load a document first."
            }

        try:
            # Prepare input for QA model
            input_text = f"question: {question} context: {self.summary}"

            # Tokenize
            inputs = self.summarizer.tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
            inputs = inputs.to(self.summarizer.device)

            # Generate answer
            with torch.no_grad():
                summary_ids = self.summarizer.model.generate(
                    inputs,
                    max_length=150,
                    min_length=5,
                    num_beams=4,
                    early_stopping=True,
                )

            # Decode answer
            answer = self.summarizer.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

            # Check if question relates to document keywords
            question_lower = question.lower()
            related_keywords = [kw for kw in self.keywords
                               if kw.lower() in question_lower]

            return {
                "success": True,
                "question": question,
                "answer": answer,
                "related_keywords": related_keywords,
                "confidence": len(related_keywords) / len(self.keywords) if self.keywords else 0
            }

        except Exception as e:
            logger.error(f"Error answering question: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def get_document_summary(self):
        """
        Get the current document summary

        Returns:
            dict: Summary information
        """
        if not self.document_context:
            return {
                "success": False,
                "error": "No document loaded"
            }

        return {
            "success": True,
            "summary": self.summary,
            "keywords": self.keywords,
            "word_count": TextProcessor.get_word_count(self.document_context),
            "reading_time": TextProcessor.get_reading_time(self.document_context)
        }

    def clear_context(self):
        """Clear loaded document context"""
        self.document_context = None
        self.summary = None
        self.keywords = []
        return {"success": True, "message": "Context cleared"}