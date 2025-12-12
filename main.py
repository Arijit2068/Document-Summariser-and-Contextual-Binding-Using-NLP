"""
Main entry point for the Document Summarizer application
Run this file to start the Flask web server
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point"""
    try:
        # Import and initialize the Flask app
        from ui.ewb_app import initialize_app
        
        logger.info("=" * 60)
        logger.info("Starting Document Summarizer & Contextual Binding")
        logger.info("=" * 60)
        
        # Initialize the application
        app = initialize_app()
        
        # Get configuration
        debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
        host = os.getenv('FLASK_HOST', '0.0.0.0')
        port = int(os.getenv('FLASK_PORT', 8080))
        
        logger.info(f"Flask app initialized successfully!")
        logger.info(f"Debug mode: {debug}")
        logger.info(f"Server will run on http://{host}:{port}")
        logger.info("=" * 60)
        logger.info("Press CTRL+C to stop the server")
        logger.info("=" * 60)
        
        # Run the application
        app.run(debug=debug, host=host, port=port)
    
    except KeyboardInterrupt:
        logger.info("\nServer stopped by user")
        sys.exit(0)
    
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
