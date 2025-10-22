#!/usr/bin/env python3
"""
Simple launcher for the healthcare chatbot
"""

if __name__ == '__main__':
    print("🏥 Starting AI Healthcare Chatbot...")
    print("🔄 Loading application...")
    
    try:
        # Import and run the app
        from app import app
        
        print("✅ Application loaded successfully!")
        print("🌐 Starting server on http://localhost:5000")
        print("📱 Open your browser and navigate to: http://localhost:5000")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        app.run(
            host='0.0.0.0',  # Listen on all interfaces
            port=5000,
            debug=False,
            use_reloader=False,
            threaded=True
        )
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("📋 Please ensure all dependencies are installed:")
        print("   pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()