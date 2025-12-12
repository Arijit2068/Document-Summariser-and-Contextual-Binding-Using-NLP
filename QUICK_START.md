# 🚀 Quick Start Guide

## Document Summarizer & Contextual Binding using NLP

Get your application running in 5 minutes!

---

## ⚡ Express Setup (macOS/Linux)

### 1. Navigate to Project
```bash
cd /Users/arijitdey/Desktop/capstone_text_summarizer_model
```

### 2. Run Setup Script
```bash
bash setup.sh
```

This will:
- ✓ Create Python virtual environment
- ✓ Install all dependencies
- ✓ Verify packages
- ✓ Check model files
- ✓ Initialize Flask app

### 3. Start the Application
```bash
source venv/bin/activate
python main.py
```

### 4. Open in Browser
```
http://localhost:5000
```

That's it! 🎉

---

## 📊 Manual Setup (if setup.sh fails)

### Step 1: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Start Server
```bash
python main.py
```

### Step 4: Access Web App
Open browser and go to `http://localhost:5000`

---

## 🎯 Try These Features

### 1. Summarize a Document
- Paste any text (minimum 50 words)
- Click "Summarize"
- View summary and keywords

### 2. Use the Chatbot
- Load a document in Chatbot tab
- Ask questions about its content
- Get contextual answers

### 3. Check History
- View all past summarizations
- Search by keyword
- Clear when needed

### 4. Try CLI
```bash
# Summarize a file
python ui/cli.py -f your_document.txt

# Extract keywords
python ui/cli.py -t "Your text" --keywords 5

# Show stats
python ui/cli.py -f document.txt --stats
```

---

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Change port
export FLASK_PORT=5001
python main.py
```

### Slow Performance
- Use GPU: Edit `app/config.py`, set `DEVICE = "cuda"`
- Reduce beam search size from 4 to 2

### Import Errors
```bash
# Verify virtual environment is activated
which python

# Should show venv path, if not:
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📚 What You Can Do

✅ **Summarize documents** of any length  
✅ **Extract keywords** automatically  
✅ **Ask chatbot questions** about documents  
✅ **Get text statistics** (words, reading time, etc.)  
✅ **Add context** to improve summaries  
✅ **View history** of all summarizations  
✅ **Download results** as text files  
✅ **Use command line** for automation  

---

## 🔗 API Endpoints

```bash
# Summarize text
curl -X POST http://localhost:5000/api/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Your document here"}'

# Extract keywords
curl -X POST http://localhost:5000/api/extract-keywords \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text", "num_keywords": 5}'

# Check health
curl http://localhost:5000/api/health
```

---

## 📖 Documentation

- **Full README**: See `README.md`
- **Installation Guide**: See `RUN_INSTRUCTIONS.md`
- **Code Structure**: See project directories

---

## 💡 Tips

1. **First Run**: Model loads on first use (takes a few seconds)
2. **Batch Processing**: Use CLI for multiple documents
3. **Best Results**: Keep documents under 2000 words
4. **GPU Support**: Install CUDA for 3-5x faster processing
5. **Mobile Friendly**: Web interface works on phones/tablets

---

## 🎓 Learning Resources

- **NLP Concepts**: Check app/utils.py for text processing
- **Model Details**: T5 Transformer (Google Research)
- **API Design**: Review ui/ewb_app.py
- **Frontend**: See ui/templates/index.html and ui/static/script.js

---

## 🆘 Need Help?

1. Check `RUN_INSTRUCTIONS.md` for detailed setup
2. Review `README.md` for comprehensive docs
3. Check `app/` for code examples
4. See error messages - they're helpful!

---

## 🎉 You're Ready!

Your Document Summarizer is now fully functional!

Enjoy using NLP technology for intelligent text analysis! 🚀

---

**Version**: 1.0.0  
**Status**: Production Ready ✅  
**Created**: 2025
