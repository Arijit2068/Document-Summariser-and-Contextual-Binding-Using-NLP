# Document Summarizer & Contextual Binding using NLP

A comprehensive web application for intelligent document summarization and contextual text analysis using state-of-the-art T5 transformer model.

## 📋 Features

- **📝 Document Summarization**: Automatically generate concise summaries of long documents
- **🔄 Contextual Binding**: Enhance summaries with optional context information
- **🔑 Keyword Extraction**: Identify key terms and important concepts
- **💬 Q&A Chatbot**: Ask questions about documents and get contextual answers
- **📊 Text Analytics**: Get detailed statistics about your documents
- **📚 History Management**: Keep track of all your summarizations
- **🎨 Modern UI**: Beautiful, responsive web interface
- **⚡ Fast Processing**: Efficient model inference on CPU and GPU

## 🏗️ Project Structure

```
capstone_text_summarizer_model/
├── app/                          # Core application modules
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration settings
│   ├── summarizer.py            # T5 summarization engine
│   ├── chatbot.py               # Q&A chatbot module
│   └── utils.py                 # Text processing utilities
├── ui/                          # Web interface
│   ├── ewb_app.py               # Flask routes and API
│   ├── cli.py                   # Command-line interface
│   ├── static/
│   │   ├── style.css            # Styling
│   │   └── script.js            # Frontend logic
│   └── templates/
│       └── index.html           # Main page
├── data/                        # Data storage
│   └── history.json             # Summarization history
├── tests/                       # Unit tests
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- 4GB+ RAM (8GB+ recommended)
- Optional: GPU with CUDA support for faster processing

### Installation

1. **Clone or download the project**
```bash
cd capstone_text_summarizer_model
```

2. **Create virtual environment** (optional but recommended)
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the Application

#### Option 1: Web Application (Recommended)

```bash
python main.py
```

The application will start at `http://localhost:5000`

#### Option 2: Command Line Interface

```bash
# Summarize a file
python ui/cli.py -f your_document.txt

# Summarize text with context
python ui/cli.py -t "Your text here" -c "Context information"

# Extract keywords
python ui/cli.py -t "Your text here" --keywords 5

# Show text statistics
python ui/cli.py -f document.txt --stats

# Save summary to file
python ui/cli.py -f document.txt -o summary.txt
```

## 📖 Usage Guide

### Web Interface

1. **Summarization**
   - Paste your document in the text area
   - Optionally add context
   - Click "Summarize" button
   - View results, keywords, and statistics

2. **Chatbot**
   - Load a document in the Chatbot tab
   - Ask questions about the document
   - Get contextual answers based on the content

3. **History**
   - View all previous summarizations
   - Search history by keyword
   - Clear history when needed

### API Endpoints

#### Summarization
```bash
POST /api/summarize
Content-Type: application/json

{
  "text": "Your document text here"
}
```

#### Contextual Summarization
```bash
POST /api/summarize-context
Content-Type: application/json

{
  "text": "Your document text",
  "context": "Optional context"
}
```

#### Keyword Extraction
```bash
POST /api/extract-keywords
Content-Type: application/json

{
  "text": "Your text",
  "num_keywords": 5
}
```

#### Chatbot Operations
```bash
# Load document
POST /api/chatbot/load
{"text": "document content"}

# Ask question
POST /api/chatbot/ask
{"question": "what is this about?"}

# Get summary
GET /api/chatbot/summary

# Clear context
POST /api/chatbot/clear
```

#### History
```bash
# Get history
GET /api/history?limit=20

# Search history
POST /api/history/search
{"keyword": "search term"}

# Clear history
POST /api/history/clear
```

#### Health Check
```bash
GET /api/health
```

## 🛠️ Configuration

Edit `app/config.py` to customize:

- Model parameters (max length, num beams, etc.)
- Device settings (CPU/GPU)
- Flask settings
- History storage

```python
class Config:
    MAX_INPUT_LENGTH = 512
    MAX_OUTPUT_LENGTH = 200
    MIN_OUTPUT_LENGTH = 30
    NUM_BEAMS = 4
    DEVICE = "cpu"  # or "cuda"
```

## 📊 Model Information

- **Model Type**: T5 (Text-To-Text Transfer Transformer)
- **Architecture**: Encoder-Decoder
- **Max Input**: 512 tokens (~2000 words)
- **Output Range**: 30-200 tokens
- **Beam Search**: 4 beams for quality generation
- **Device**: CPU/GPU compatible

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

Test files included:
- `tests/test_summarizer.py` - Summarization tests
- `tests/test_chatbot.py` - Chatbot tests
- `tests/test_utility.py` - Utility function tests

## 📝 Example Usage

### Example 1: Simple Summarization

```python
from app.summarizer import DocumentSummarizer
from app.config import Config

# Initialize
summarizer = DocumentSummarizer(
    model_path='model.safetensors',
    tokenizer_path='.',
    device='cpu',
    config=Config
)

# Summarize
text = "Your long document here..."
result = summarizer.summarize(text)
print(result['summary'])
```

### Example 2: Extract Keywords

```python
from app.utils import ContextBinder

text = "Your document here..."
keywords = ContextBinder.extract_keywords(text, num_keywords=5)
print(keywords)  # ['keyword1', 'keyword2', ...]
```

### Example 3: Text Statistics

```python
from app.utils import TextProcessor

text = "Your document here..."
word_count = TextProcessor.get_word_count(text)
reading_time = TextProcessor.get_reading_time(text)
sentences = TextProcessor.split_sentences(text)
```

## 📦 Dependencies

- **Flask 2.3.3** - Web framework
- **transformers 4.37.2** - NLP models
- **torch 2.0.1** - Deep learning framework
- **NLTK 3.8.1** - Text processing
- **NumPy 1.24.3** - Numerical computing

See `requirements.txt` for complete list.

## 🎯 Performance

**CPU Performance** (Intel i5/Ryzen 5):
- Small document (500 words): ~5-10 seconds
- Medium document (1500 words): ~8-15 seconds
- Large document (2000+ words): ~15-20 seconds

**GPU Performance** (NVIDIA GPU):
- 3-5x faster than CPU

**Memory Usage**:
- Model: ~1.2GB
- Runtime: 2-4GB

## 🐛 Troubleshooting

### Model not loading
```
Error: Could not load custom model
Solution: Ensure model.safetensors is in the project root
```

### Out of memory
```
Error: CUDA out of memory
Solution: Use CPU instead (set DEVICE="cpu" in config) or reduce batch size
```

### Port already in use
```
Error: Address already in use
Solution: Change port - python main.py --port 5001
```

### Slow summarization
```
Solution: 
1. Use GPU if available
2. Reduce input length
3. Reduce num_beams to 2
```

## 📈 Future Enhancements

- [ ] Support for multiple languages
- [ ] Document upload/drag-and-drop
- [ ] Export to PDF/Word
- [ ] Batch processing
- [ ] Advanced NER and relation extraction
- [ ] Custom model fine-tuning
- [ ] Docker containerization
- [ ] Database integration for large-scale history

## 👥 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is provided as-is for educational and commercial use.

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the example code
3. Check API endpoint documentation

## 🎓 Educational Use

This application demonstrates:
- NLP and text processing
- Transformer-based models (T5)
- Flask web application development
- RESTful API design
- Frontend-backend integration
- Chatbot implementation

## ⭐ Acknowledgments

- T5 Model by Google Research
- Transformers library by Hugging Face
- Flask web framework
- PyTorch deep learning framework

---

**Created**: 2025  
**Last Updated**: November 25, 2025  
**Version**: 1.0.0
