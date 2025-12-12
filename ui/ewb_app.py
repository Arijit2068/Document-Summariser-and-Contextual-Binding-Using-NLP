"""
Flask web application for Document Summarizer
Main Flask app with routes and API endpoints
"""

import os
import logging
import torch
from flask import Flask, render_template, request, jsonify, send_from_directory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import app components
from app import create_app
from dev_fix import FixedDocumentSummarizer as DocumentSummarizer
from app.chatbot import DocumentChatbot
from app.utils import TextProcessor, ContextBinder, HistoryManager

# Create Flask app instance so route decorators work at import time
app = create_app()
"""
Flask web application for Document Summarizer
Main Flask app with routes and API endpoints
"""

import os
import logging
import torch
from flask import Flask, render_template, request, jsonify, send_from_directory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import app components
from app import create_app
from dev_fix import FixedDocumentSummarizer as DocumentSummarizer
from app.chatbot import DocumentChatbot
from app.utils import TextProcessor, ContextBinder, HistoryManager

# Create Flask app instance so route decorators work at import time
app = create_app()
summarizer = None
chatbot = None
history_manager = None

def initialize_app():
    """Initialize the Flask app and all components"""
    global app, summarizer, chatbot, history_manager
    # Note: `app` is created at import time so route decorators are bound.
    
    # Set up logging
    if not app.debug:
        file_handler = logging.FileHandler('app.log')
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
    
    global summarizer, chatbot, history_manager
    # Initialize summarizer
    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(project_root, 'model.safetensors')
        tokenizer_path = project_root

        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {device}")

        summarizer = DocumentSummarizer(model_path, tokenizer_path, device, config=app.config)
        logger.info("Summarizer initialized successfully!")

    except Exception as e:
        logger.error(f"Error initializing summarizer: {e}")
        summarizer = None

    # Initialize chatbot
    if summarizer:
        chatbot = DocumentChatbot(summarizer)
        logger.info("Chatbot initialized successfully!")
    else:
        chatbot = None

    # Initialize history manager
    try:
        history_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                   'data', 'history.json')
        history_manager = HistoryManager(history_file)
        logger.info("History manager initialized successfully!")
    except Exception as e:
        logger.error(f"Error initializing history manager: {e}")
        history_manager = None

    return app


def get_app():
    """Get or create the Flask app"""
    global app
    if app is None:
        initialize_app()
    return app


# Routes
@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/summarize', methods=['POST'])
def summarize():
    """API endpoint for summarization"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        if not summarizer:
            return jsonify({"error": "Summarizer not initialized"}), 500
        
        # Clean text
        text = TextProcessor.clean_text(text)
        
        # Summarize
        result = summarizer.summarize(text)
        
        if result.get("error"):
            return jsonify(result), 400
        
        # Extract keywords
        keywords = ContextBinder.extract_keywords(text, num_keywords=5)
        result["keywords"] = keywords
        
        # Save to history
        if history_manager:
            history_manager.add_entry(
                text,
                result.get('summary', ''),
                keywords=keywords
            )
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error in summarize endpoint: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/summarize-context', methods=['POST'])
def summarize_with_context():
    """API endpoint for contextual summarization"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        context = data.get('context', '').strip()
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        if not summarizer:
            return jsonify({"error": "Summarizer not initialized"}), 500
        
        text = TextProcessor.clean_text(text)
        context = TextProcessor.clean_text(context) if context else None
        
        result = summarizer.summarize_with_context(text, context)
        
        if result.get("error"):
            return jsonify(result), 400
        
        keywords = ContextBinder.extract_keywords(text, num_keywords=5)
        result["keywords"] = keywords
        
        if history_manager:
            history_manager.add_entry(text, result.get('summary', ''), context, keywords)
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error in summarize-context endpoint: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/extract-keywords', methods=['POST'])
def extract_keywords():
    """API endpoint for keyword extraction"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        num_keywords = data.get('num_keywords', 5)
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        text = TextProcessor.clean_text(text)
        keywords = ContextBinder.extract_keywords(text, num_keywords)
        
        return jsonify({"keywords": keywords}), 200
    
    except Exception as e:
        logger.error(f"Error in extract-keywords endpoint: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/text-info', methods=['POST'])
def text_info():
    """API endpoint for text information"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        text = TextProcessor.clean_text(text)
        
        info = {
            "word_count": TextProcessor.get_word_count(text),
            "reading_time": TextProcessor.get_reading_time(text),
            "sentence_count": len(TextProcessor.split_sentences(text)),
            "paragraph_count": len(TextProcessor.split_paragraphs(text))
        }
        
        return jsonify(info), 200
    
    except Exception as e:
        logger.error(f"Error in text-info endpoint: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/chatbot/load', methods=['POST'])
def chatbot_load():
    """API endpoint to load document for chatbot"""
    try:
        if not chatbot:
            return jsonify({"error": "Chatbot not initialized"}), 500
        
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        text = TextProcessor.clean_text(text)
        result = chatbot.load_document(text)
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error in chatbot-load endpoint: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/chatbot/ask', methods=['POST'])
def chatbot_ask():
    """API endpoint for chatbot question answering"""
    try:
        if not chatbot:
            return jsonify({"error": "Chatbot not initialized"}), 500
        
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({"error": "No question provided"}), 400
        
        result = chatbot.answer_question(question)
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error in chatbot-ask endpoint: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/chatbot/summary', methods=['GET'])
def chatbot_summary():
    """API endpoint to get current chatbot summary"""
    try:
        if not chatbot:
            return jsonify({"error": "Chatbot not initialized"}), 500
        
        result = chatbot.get_document_summary()
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error in chatbot-summary endpoint: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/chatbot/clear', methods=['POST'])
def chatbot_clear():
    """API endpoint to clear chatbot context"""
    try:
        if not chatbot:
            return jsonify({"error": "Chatbot not initialized"}), 500
        
        result = chatbot.clear_context()
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error in chatbot-clear endpoint: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """API endpoint to get summarization history"""
    try:
        if not history_manager:
            return jsonify({"error": "History manager not initialized"}), 500
        
        limit = request.args.get('limit', 20, type=int)
        history = history_manager.get_history(limit=limit)
        
        return jsonify({"history": history}), 200
    
    except Exception as e:
        logger.error(f"Error in history endpoint: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/history/search', methods=['POST'])
def search_history():
    """API endpoint to search history"""
    try:
        if not history_manager:
            return jsonify({"error": "History manager not initialized"}), 500
        
        data = request.get_json()
        keyword = data.get('keyword', '').strip()
        
        if not keyword:
            return jsonify({"error": "No keyword provided"}), 400
        
        results = history_manager.search_history(keyword)
        
        return jsonify({"results": results}), 200
    
    except Exception as e:
        logger.errorf("Error in history-search endpoint: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/history/clear', methods=['POST'])
def clear_history():
    """API endpoint to clear history"""
    try:
        if not history_manager:
            return jsonify({"error": "History manager not initialized"}), 500
        
        success = history_manager.clear_history()
        
        return jsonify({"success": success, "message": "History cleared"}), 200
    
    except Exception as e:
        logger.error(f"Error clearing history: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    status = {
        "status": "ok",
        "summarizer": summarizer is not None,
        "chatbot": chatbot is not None,
        "history_manager": history_manager is not None
    }
    return jsonify(status), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app = initialize_app()
    app.run(debug=True, host='0.0.0.0', port=5000)


