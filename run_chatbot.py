#!/usr/bin/env python3
"""
Alternative server launcher with better error handling
"""

import socket
import sys
from contextlib import closing

def check_port(host, port):
    """Check if a port is available"""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        return result != 0

def find_available_port(start_port=5000, max_attempts=10):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        if check_port('localhost', port):
            return port
    return None

if __name__ == '__main__':
    print("🏥 AI Healthcare Chatbot - Alternative Launcher")
    print("=" * 50)
    
    try:
        # Import and configure the app
        from app import app
        
        # Find available port
        port = find_available_port(5000)
        if not port:
            print("❌ No available ports found. Please close other applications using ports 5000-5010")
            sys.exit(1)
        
        host = '0.0.0.0'
        
        print(f"✅ Application loaded successfully!")
        print(f"🌐 Starting server on http://localhost:{port}")
        print(f"📱 Open your browser and navigate to: http://localhost:{port}")
        if port != 5000:
            print(f"ℹ️  Note: Using port {port} instead of 5000")
        print(f"⏹️  Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Configure Flask app
        app.config['SERVER_NAME'] = None
        app.config['APPLICATION_ROOT'] = '/'
        
        # Start the server
        app.run(
            host=host,
            port=port,
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
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use!")
            print("💡 Try closing other applications or use a different port")
        else:
            print(f"❌ Network error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()