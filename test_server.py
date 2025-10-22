#!/usr/bin/env python3
"""
Simple Flask server with built-in testing
"""

from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import re, random, pandas as pd, numpy as np, csv, warnings, os
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from difflib import get_close_matches

# Simple test route
app = Flask(__name__)
app.secret_key = "supersecret"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/test')
def test():
    return "Server is working! ✅"

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Healthcare Chatbot Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f0f8ff; }
            .container { max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            h1 { color: #007bff; text-align: center; }
            .status { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }
            button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            button:hover { background: #0056b3; }
            .chat-area { border: 1px solid #ddd; height: 400px; padding: 10px; overflow-y: auto; background: #f9f9f9; }
            input { width: 70%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏥 AI Healthcare Chatbot</h1>
            <div class="status">
                ✅ Server Status: Running Successfully!<br>
                ✅ Port: 5000<br>
                ✅ Access: http://localhost:5000
            </div>
            
            <div id="chat-area" class="chat-area">
                <div><strong>Bot:</strong> Welcome to the Healthcare Chatbot! 🤖</div>
                <div><strong>Bot:</strong> What is your name?</div>
            </div>
            
            <input type="text" id="user-input" placeholder="Type your message here..." onkeypress="if(event.key==='Enter') sendMessage()">
            <button onclick="sendMessage()">Send</button>
            <button onclick="location.reload()">Restart</button>
            
            <script>
                function sendMessage() {
                    const input = document.getElementById('user-input');
                    const chatArea = document.getElementById('chat-area');
                    
                    if (input.value.trim()) {
                        chatArea.innerHTML += '<div><strong>You:</strong> ' + input.value + '</div>';
                        chatArea.innerHTML += '<div><strong>Bot:</strong> Thank you for your message! This is a test version. The full chatbot functionality is being set up.</div>';
                        input.value = '';
                        chatArea.scrollTop = chatArea.scrollHeight;
                    }
                }
            </script>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("🧪 Starting Test Server...")
    print("📱 Open browser: http://localhost:5000")
    
    try:
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=True,
            use_reloader=False
        )
    except Exception as e:
        print(f"Error: {e}")