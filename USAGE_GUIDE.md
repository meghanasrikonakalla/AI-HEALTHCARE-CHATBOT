# 🚀 HOW TO RUN THE AI HEALTHCARE CHATBOT

## Quick Start (Windows)

### Method 1: Double-click the batch file
1. Simply double-click `start_chatbot.bat`
2. Wait for the server to start (you'll see "Running on http://localhost:5000")
3. Open your browser and go to: http://localhost:5000

### Method 2: Using Python directly
1. Open Command Prompt or PowerShell
2. Navigate to the project folder:
   ```
   cd "c:\Web Development\ai-health-care\AI-Health-Chatbot-Web-integration-main"
   ```
3. Run the server:
   ```
   python start_server.py
   ```
4. Open your browser and go to: http://localhost:5000

### Method 3: Using the original app.py
1. Open Command Prompt or PowerShell
2. Navigate to the project folder
3. Run:
   ```
   python app.py
   ```
4. Open your browser and go to: http://localhost:5000

## 🏥 Using the Healthcare Chatbot

Once the server is running and you've opened http://localhost:5000 in your browser:

1. **Welcome Screen**: You'll see a chat interface with a welcome message
2. **Start Consultation**: The bot will ask for your name
3. **Provide Information**: Answer questions about:
   - Personal details (name, age, gender)
   - Symptoms description (e.g., "I have fever and headache")
   - Duration of symptoms
   - Severity level (1-10 scale)
   - Medical history
   - Lifestyle factors

4. **Guided Assessment**: Answer specific symptom-related questions
5. **Get Results**: Receive comprehensive health assessment with:
   - Predicted condition
   - Confidence percentage
   - Detailed description
   - Recommended precautions

## 🔄 Restarting a Consultation

- Click the restart button (🔄) in the top-right corner
- Or refresh the browser page

## ⏹️ Stopping the Server

- Press `Ctrl+C` in the terminal window
- Or close the Command Prompt/PowerShell window

## 🐛 Troubleshooting

### If you get "Connection Refused" error:
1. Make sure the server is running (check the terminal window)
2. Wait a few seconds for the server to fully start
3. Try refreshing the browser page
4. Check that you're using http://localhost:5000 (not https)

### If you get Python errors:
1. Make sure all dependencies are installed:
   ```
   pip install -r requirements.txt
   ```
2. Check that you're using Python 3.8 or higher

### If the chatbot doesn't respond:
1. Check the terminal for error messages
2. Try restarting the server
3. Make sure you're entering valid responses

## 📱 Browser Compatibility

The chatbot works best with:
- Chrome (recommended)
- Firefox
- Safari
- Edge

## 🎯 Features

- **42 Different Health Conditions** supported
- **Natural Language Processing** for symptom extraction
- **Machine Learning Predictions** with confidence scores
- **Personalized Recommendations** based on your input
- **Mobile-Friendly Interface**
- **Real-time Chat Experience**

## ⚠️ Important Disclaimer

This AI healthcare chatbot is for informational purposes only and should not replace professional medical advice. Always consult with qualified healthcare professionals for medical decisions.

---

**Enjoy using your AI Healthcare Chatbot! 🏥✨**