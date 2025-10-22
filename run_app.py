#!/usr/bin/env python3
"""
Simple script to run the healthcare chatbot application
"""

import sys
import os
from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("🏥 AI HEALTHCARE CHATBOT - STARTING UP")
    print("=" * 60)
    print(f"🐍 Python Version: {sys.version}")
    print(f"📁 Working Directory: {os.getcwd()}")
    print(f"🌐 Server URL: http://localhost:5000")
    print(f"🔧 Debug Mode: Enabled")
    print("=" * 60)
    print("🚀 Starting Flask server...")
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000, 
            debug=True,
            use_reloader=False  # Disable reloader to prevent double startup
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()