#!/bin/bash

# Document Summarizer - Setup and Verification Script
# This script helps with installation and verification

set -e

echo "=================================="
echo "Document Summarizer Setup Script"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "📋 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python3 not found${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}"

# Create virtual environment
echo ""
echo "🔧 Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}ℹ Virtual environment already exists${NC}"
fi

# Activate virtual environment
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Upgrade pip
echo ""
echo "📦 Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓ pip upgraded${NC}"

# Install requirements
echo ""
echo "📥 Installing dependencies..."
if pip install -r requirements.txt > /tmp/pip_install.log 2>&1; then
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${RED}✗ Failed to install dependencies${NC}"
    cat /tmp/pip_install.log
    exit 1
fi

# Verify imports
echo ""
echo "✅ Verifying package imports..."
if python3 << 'EOF'
import sys
try:
    import flask
    import transformers
    import torch
    import nltk
    import numpy
    print("All packages imported successfully")
    sys.exit(0)
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)
EOF
then
    echo -e "${GREEN}✓ All packages verified${NC}"
else
    echo -e "${RED}✗ Package verification failed${NC}"
    exit 1
fi

# Check model file
echo ""
echo "🤖 Checking model file..."
if [ -f "model.safetensors" ]; then
    SIZE=$(du -h model.safetensors | cut -f1)
    echo -e "${GREEN}✓ Model file found (${SIZE})${NC}"
else
    echo -e "${YELLOW}⚠ Model file not found (model.safetensors)${NC}"
    echo -e "${YELLOW}  The application will use the default T5-base model${NC}"
fi

# Check tokenizer files
echo ""
echo "📚 Checking tokenizer files..."
TOKENIZER_FILES=("tokenizer.json" "special_tokens_map.json" "tokenizer_config.json" "spiece.model")
for file in "${TOKENIZER_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ $file found${NC}"
    else
        echo -e "${YELLOW}⚠ $file not found (using default)${NC}"
    fi
done

# Create data directory
echo ""
echo "📁 Setting up data directories..."
mkdir -p data
mkdir -p ui/static
mkdir -p ui/templates
echo -e "${GREEN}✓ Directories ready${NC}"

# Test Flask app
echo ""
echo "🧪 Testing Flask app initialization..."
if python3 << 'EOF'
import sys
import os
sys.path.insert(0, os.getcwd())

try:
    from app import create_app
    app = create_app()
    print("Flask app initialized successfully")
    sys.exit(0)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
EOF
then
    echo -e "${GREEN}✓ Flask app initialized successfully${NC}"
else
    echo -e "${RED}✗ Flask app initialization failed${NC}"
fi

# Print next steps
echo ""
echo "=================================="
echo -e "${GREEN}Setup completed successfully!${NC}"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Start the web application:"
echo "   python main.py"
echo ""
echo "3. Open in browser:"
echo "   http://localhost:5000"
echo ""
echo "4. Or use the CLI:"
echo "   python ui/cli.py --help"
echo ""
echo "For more information, see README.md"
echo ""
