#!/usr/bin/env python3
"""
AWS Entry Point for AI Resume Screener
This file serves as the main entry point for AWS deployment
"""

import os
import sys
from run import app

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# AWS-specific configurations
if __name__ == '__main__':
    # Get port from environment variable (AWS sets this)
    port = int(os.environ.get('PORT', 8000))
    
    # Get host from environment variable
    host = os.environ.get('HOST', '0.0.0.0')
    
    # Disable debug in production
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"Starting AI Resume Screener on {host}:{port}")
    print(f"Debug mode: {debug}")
    
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True  # Enable threading for better performance
    )
