"""
Command Line Interface for Document Summarizer
Quick access to summarization features from terminal
"""

import argparse
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.summarizer import DocumentSummarizer
from app.utils import TextProcessor, ContextBinder, HistoryManager


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Document Summarizer & Contextual Binding CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Summarize a file
  python cli.py -f document.txt
  
  # Summarize text with context
  python cli.py -t "Your text here" -c "Context here"
  
  # Extract keywords
  python cli.py -t "Your text here" --keywords 5
  
  # Get text statistics
  python cli.py -f document.txt --stats
        '''
    )
    
    parser.add_argument('-f', '--file', type=str, help='Path to text file to summarize')
    parser.add_argument('-t', '--text', type=str, help='Text to summarize')
    parser.add_argument('-c', '--context', type=str, help='Context for summarization')
    parser.add_argument('--keywords', type=int, nargs='?', const=5, help='Extract N keywords')
    parser.add_argument('--stats', action='store_true', help='Show text statistics')
    parser.add_argument('--length', type=int, help='Maximum summary length')
    parser.add_argument('-o', '--output', type=str, help='Output file path')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.file and not args.text:
        parser.print_help()
        sys.exit(1)
    
    # Get text to process
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found")
            sys.exit(1)
    else:
        text = args.text
    
    # Clean text
    text = TextProcessor.clean_text(text)
    
    if not text.strip():
        print("Error: No text provided")
        sys.exit(1)
    
    # Initialize summarizer
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(project_root, 'model.safetensors')
    tokenizer_path = project_root
    
    print("Loading model...")
    summarizer = DocumentSummarizer(model_path, tokenizer_path)
    
    # Show statistics if requested
    if args.stats:
        print("\n" + "="*60)
        print("TEXT STATISTICS")
        print("="*60)
        print(f"Word Count: {TextProcessor.get_word_count(text)}")
        print(f"Reading Time: {TextProcessor.get_reading_time(text)} minutes")
        sentences = TextProcessor.split_sentences(text)
        print(f"Sentence Count: {len(sentences)}")
        paragraphs = TextProcessor.split_paragraphs(text)
        print(f"Paragraph Count: {len(paragraphs)}")
    
    # Extract keywords if requested
    if args.keywords is not None:
        print("\n" + "="*60)
        print(f"TOP {args.keywords} KEYWORDS")
        print("="*60)
        keywords = ContextBinder.extract_keywords(text, args.keywords)
        for i, kw in enumerate(keywords, 1):
            print(f"{i}. {kw}")
    
    # Summarize
    if args.text or args.file:
        print("\n" + "="*60)
        print("SUMMARIZATION")
        print("="*60)
        print("Processing...")
        
        result = summarizer.summarize_with_context(text, args.context, args.length)
        
        if result.get('error'):
            print(f"Error: {result['error']}")
            sys.exit(1)
        
        summary = result.get('summary', '')
        print(f"\nOriginal Length: {result.get('original_length', 0)} words")
        print(f"Summary Length: {result.get('summary_length', 0)} words")
        print(f"Compression Ratio: {result.get('compression_ratio', 0)}x\n")
        print("SUMMARY:")
        print("-" * 60)
        print(summary)
        print("-" * 60)
        
        # Save to file if requested
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(summary)
            print(f"\nSummary saved to: {args.output}")


if __name__ == '__main__':
    main()
