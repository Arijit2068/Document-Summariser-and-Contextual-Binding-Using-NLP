# Document Summarizer - Installation and Run Instructions

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 4GB RAM minimum (8GB recommended)
- Optional: GPU with CUDA support for faster processing

## 🔧 Installation Steps

### Step 1: Set Up Python Environment

**macOS/Linux:**
```bash
# Navigate to project directory
cd /Users/arijitdey/Desktop/capstone_text_summarizer_model

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

**Windows:**
```bash
cd capstone_text_summarizer_model
python -m venv venv
venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

This will install:
- Flask 2.3.3
- Transformers 4.37.2
- PyTorch 2.0.1
- NLTK 3.8.1
- NumPy 1.24.3
- And other dependencies

## ✅ Verify Installation

```bash
# Test imports
python -c "import flask, transformers, torch; print('✓ All packages installed correctly')"

# Check if model file exists
ls model.safetensors
```

## 🚀 Running the Application

### Option 1: Start Web Server (Recommended)

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Run the Flask application
python main.py
```

**Expected output:**
```
INFO:__main__:============================================================
INFO:__main__:Starting Document Summarizer & Contextual Binding
INFO:__main__:============================================================
INFO:__main__:Using device: cpu
INFO:__main__:Summarizer initialized successfully!
INFO:__main__:Chatbot initialized successfully!
INFO:__main__:History manager initialized successfully!
INFO:__main__:Flask app initialized successfully!
INFO:__main__:Debug mode: True
INFO:__main__:Server will run on http://0.0.0.0:5000
============================================================
Press CTRL+C to stop the server
============================================================
```

### Open in Browser

Open your web browser and go to:
```
http://localhost:5000
```

You should see the Document Summarizer interface!

### Option 2: Command Line Interface

```bash
# Summarize a file
python ui/cli.py -f your_document.txt

# Summarize text with output
python ui/cli.py -t "Your text here" -o summary.txt

# Extract keywords
python ui/cli.py -t "Your text here" --keywords 5

# Show statistics
python ui/cli.py -f document.txt --stats
```

## 🌐 Web Interface Features

Once the server is running, you can:

1. **Summarizer Tab**
   - Paste documents
   - Add optional context
   - Get instant summaries
   - Extract keywords
   - Download results

2. **Chatbot Tab**
   - Load documents
   - Ask questions
   - Get contextual answers

3. **History Tab**
   - View past summarizations
   - Search history
   - Export results

4. **About Tab**
   - Learn about features
   - Technology stack
   - Usage guide

## 📊 API Testing

Test endpoints using curl or Postman:

```bash
# Simple summarization
curl -X POST http://localhost:5000/api/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Your document text here..."}'

# Get health status
curl http://localhost:5000/api/health
```

## 🛠️ Configuration

### Change Port
```bash
# Edit main.py or set environment variable
export FLASK_PORT=8000
python main.py
```

### Use GPU (if available)
```bash
# Edit app/config.py
# Change: DEVICE = "cpu"
# To:     DEVICE = "cuda"
```

### Debug Mode
```bash
export FLASK_DEBUG=True
python main.py
```

## 📁 Project Structure

```
capstone_text_summarizer_model/
├── app/                      # Core application
│   ├── __init__.py          # App factory
│   ├── config.py            # Configuration
│   ├── summarizer.py        # T5 summarizer
│   ├── chatbot.py           # Q&A chatbot
│   └── utils.py             # Utilities
├── ui/                      # Web interface
│   ├── ewb_app.py           # Flask routes
│   ├── cli.py               # CLI interface
│   ├── static/              # CSS and JS
│   └── templates/           # HTML
├── data/                    # Data storage
│   └── history.json         # Summarization history
├── tests/                   # Unit tests
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
└── README.md               # Full documentation
```

## 🧪 Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_summarizer.py -v

# Run with coverage
python -m pytest tests/ --cov=app/
```

## 🐛 Common Issues and Solutions

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate
# Reinstall requirements
pip install -r requirements.txt
```

### Issue: "CUDA out of memory"
**Solution:**
1. Use CPU instead of GPU
2. Edit `app/config.py` and set `DEVICE = "cpu"`
3. Restart the application

### Issue: "Port 5000 already in use"
**Solution:**
```bash
# Change port in main.py or use:
export FLASK_PORT=5001
python main.py
```

### Issue: Model not loading
**Solution:**
```bash
# Verify model file exists
ls -la model.safetensors
# File should be ~2.4GB
```

### Issue: Slow summarization
**Solution:**
1. Check if using GPU: `DEVICE = "cuda"`
2. Reduce `NUM_BEAMS` from 4 to 2 in config
3. Use shorter documents (< 1000 words)

## 🚦 Stopping the Server

Press `CTRL+C` in the terminal where Flask is running.

## 📈 Performance Tips

1. **Use GPU** if available for 3-5x speed improvement
2. **Batch requests** for multiple documents
3. **Cache results** for frequently summarized documents
4. **Reduce beam search** size for faster results
5. **Use shorter documents** for better performance

## 📚 Documentation

- Full documentation: See `README.md`
- API documentation: Available at `/api/health`
- Code examples: See `app/` directory

## 🆘 Need Help?

1. Check README.md for detailed documentation
2. Review example code in the app directory
3. Check API documentation
4. Examine error messages carefully
5. Try with a simple test document first

## ✨ Next Steps

After successful installation:

1. **Test the web interface** at http://localhost:5000
2. **Try example documents** in the web app
3. **Explore the chatbot** feature
4. **Check your summarization history**
5. **Download summaries** as text files

## 📝 Example Usage

### Web Interface
1. Navigate to http://localhost:5000
2. Click on "Summarizer" tab
3. Paste a document (minimum 50 words)
4. Click "Summarize"
5. View results and keywords

### CLI Usage
```bash
# Summarize a document file
python ui/cli.py -f ~/Documents/article.txt

# Save summary to file
python ui/cli.py -t "Your document..." -o summary.txt

# Extract top 10 keywords
python ui/cli.py -t "Your document..." --keywords 10
```

---

**Version**: 1.0.0  
**Last Updated**: November 25, 2025  
**Status**: Production Ready ✅
