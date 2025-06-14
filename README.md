# 🤖 Sage AI - Advanced Voice Assistant

<div align="center">

![Sage AI Logo](https://img.shields.io/badge/Sage%20AI-Advanced%20Assistant-blue?style=for-the-badge&logo=robot)

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://python.org)
[![AI Models](https://img.shields.io/badge/AI-Gemini%202.5%20%7C%20Mistral-green?style=flat-square)](https://github.com/Sagexd08/Sage-AI)
[![Voice Control](https://img.shields.io/badge/Voice-Enabled-orange?style=flat-square&logo=microphone)](https://github.com/Sagexd08/Sage-AI)
[![License](https://img.shields.io/badge/License-Private-red?style=flat-square)](https://github.com/Sagexd08/Sage-AI)

**A next-generation AI-powered voice assistant with dual AI model support, advanced voice recognition, and comprehensive system integration.**

[🚀 Quick Start](#-quick-start) • [📖 Documentation](#-features) • [🎯 Commands](#-voice-commands) • [⚙️ Setup](#️-installation--setup)

</div>

---

## 🌟 Overview

Sage AI is a sophisticated voice assistant that combines the power of **Google Gemini 2.5 Flash** and **Mistral AI** to deliver intelligent, context-aware responses. Built with advanced speech recognition, system integration, and a beautiful console interface, Sage AI represents the future of personal AI assistants.

### 🎯 Key Highlights

- **🧠 Dual AI Models**: Choose between Gemini 2.5 Flash and Mistral 7B for different conversation styles
- **🎤 Advanced Voice Recognition**: Real-time speech processing with noise filtering and wake word detection
- **📱 Camera Integration**: Direct camera access and control
- **🎵 Multi-Platform Music**: Spotify, YouTube Music, and Apple Music integration
- **📧 Smart Email Management**: AI-powered email composition and contact management
- **🖥️ System Control**: Launch applications, open websites, and control Windows features
- **💾 Persistent Memory**: SQLite database for conversation history and user preferences
- **🎨 Beautiful Interface**: Rich console output with colors, panels, and real-time status

## ✨ Features

### 🎤 **Advanced Voice Control**
- **Wake Word Detection**: "Sage", "Hey Sage", "Jarvis" activation
- **Continuous Listening Mode**: Hands-free operation
- **Noise Filtering**: Automatic ambient noise adjustment
- **Multi-Language Support**: English (US/IN) recognition
- **Timeout Handling**: Smart conversation flow management

### 🧠 **Dual AI Intelligence**
- **Gemini 2.5 Flash**: Google's latest AI model for natural conversations
- **Mistral 7B**: Powerful language model for detailed responses
- **Dynamic Model Switching**: Change AI models on-the-fly
- **Context Retention**: Maintains conversation history across sessions
- **Personalized Responses**: Tailored to user preferences and patterns

### 📱 **Camera & Media Control**
- **Instant Camera Access**: Voice-activated camera opening
- **Multiple Fallback Methods**: Ensures camera always opens
- **Windows Integration**: Native Windows Camera app support
- **Voice Feedback**: Confirmation and status updates

### 🎵 **Music Integration**
- **Spotify**: Direct app launching and web fallback
- **YouTube Music**: Search and play functionality
- **Apple Music**: Cross-platform music access
- **Voice Commands**: "Play [song] on [platform]"
- **Smart Search**: Optimized query handling

### 📧 **Intelligent Email System**
- **AI-Powered Composition**: Context-aware email generation
- **Contact Management**: Voice-activated contact selection
- **Professional Templates**: Business and personal email styles
- **Gmail Integration**: SMTP with app password support
- **Voice Dictation**: Speak your emails naturally

### 🖥️ **System Integration**
- **Application Launcher**: Voice-controlled app opening
- **Web Navigation**: Direct website access
- **Windows Features**: Settings, Control Panel, Task Manager
- **Browser Control**: Chrome, Firefox, Edge support
- **File System**: Explorer and file management

### 💾 **Data Management**
- **SQLite Database**: Persistent conversation storage
- **User Preferences**: Customizable settings and behaviors
- **Conversation History**: Searchable chat logs
- **Reminder System**: Voice-activated reminders and notes
- **Backup & Restore**: Data persistence across sessions

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** installed on your system
- **Microphone** for voice input
- **Internet connection** for AI models
- **Windows 10/11** (optimized for Windows)

### ⚡ One-Command Setup
```bash
git clone https://github.com/Sagexd08/Sage-AI.git
cd Sage-AI
python deploy.py
```

### 🔧 Manual Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Sagexd08/Sage-AI.git
   cd Sage-AI
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys**
   ```bash
   # Edit config.py with your API keys
   notepad config.py  # Windows
   nano config.py     # Linux/Mac
   ```

4. **Launch Sage AI**
   ```bash
   python main.py
   ```

## ⚙️ Installation & Setup

### 🔑 API Configuration

#### Required API Keys
1. **Google Gemini API Key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add to `config.py`: `gemini_api_key = "your_key_here"`

2. **OpenRouter API Key** (for Mistral)
   - Visit [OpenRouter](https://openrouter.ai/keys)
   - Create account and generate key
   - Add to `config.py`: `apikey = "your_key_here"`

#### Email Configuration (Optional)
```python
EMAIL_CONFIG = {
    "from_email": "your_email@gmail.com",
    "password": "your_app_password",  # Gmail App Password
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587
}
```

#### Contact Management
```python
CONTACTS = {
    "mom": "mom@example.com",
    "dad": "dad@example.com",
    "friend": "friend@example.com",
    "work": "work@company.com"
}
```

### 🎤 Audio Setup

#### Windows Audio Configuration
1. **Microphone Permissions**
   - Settings → Privacy → Microphone
   - Enable microphone access for Python

2. **Audio Drivers**
   - Ensure latest audio drivers are installed
   - Test microphone in Windows Sound settings

3. **PyAudio Installation** (if issues occur)
   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```

## 🎯 Voice Commands

### 🎵 **Music Control**
```
🎵 Music Commands:
├── "Play [song name] on Spotify"
├── "Play music on YouTube"
├── "Open Apple Music"
├── "Play [artist] songs"
└── "Open Spotify"
```

### 📧 **Email Management**
```
📧 Email Commands:
├── "Send email to [contact]"
├── "Email [contact] about [topic]"
├── "Compose email"
└── "Check email"
```

### 🖥️ **System Control**
```
🖥️ System Commands:
├── "Open [application]"
├── "Launch calculator"
├── "Open camera"
├── "Start notepad"
├── "Open file explorer"
└── "Task manager"
```

### 🌐 **Web Navigation**
```
🌐 Web Commands:
├── "Open Google"
├── "YouTube"
├── "Gmail"
├── "Search for [query]"
└── "Open [website]"
```

### 🤖 **AI Interaction**
```
🤖 AI Commands:
├── "Change AI model"
├── "Which AI are you using?"
├── "Switch to Gemini"
├── "Use Mistral"
└── "Continuous mode on/off"
```

### 🔄 **System Control**
```
🔄 Control Commands:
├── "What time is it?"
├── "Goodbye" / "Exit" / "Bye"
├── "Continuous mode on"
├── "Stop listening"
└── "Help"
```

## 🏗️ Architecture

```
📁 Sage AI Project Structure
├── 🧠 main.py                 # Core AI assistant with dual model support
├── ⚙️ config.py               # API keys and configuration
├── 🚀 deploy.py               # Automated deployment script
├── 📋 requirements.txt        # Python dependencies
├── 🗃️ sage_data.db           # SQLite database (auto-created)
├── 📝 sage.log               # Application logs
├── 🔧 sage_advanced.py        # Advanced AI functions (legacy)
├── 🎯 launch_sage.bat         # Windows batch launcher
└── 🧪 test_voice.py          # Voice recognition testing
```

### 🔧 **Core Components**

#### 🧠 AdvancedSageAI Class
- **Initialization**: Multi-component setup with error handling
- **Voice Processing**: Advanced speech recognition with noise filtering
- **AI Integration**: Dual model support with dynamic switching
- **Command Processing**: Intelligent intent recognition and routing
- **Database Management**: SQLite operations for persistence

#### 🎤 Voice Recognition Engine
- **Speech-to-Text**: Google Speech Recognition with fallbacks
- **Wake Word Detection**: Multiple activation phrases
- **Noise Filtering**: Automatic ambient noise adjustment
- **Timeout Management**: Smart conversation flow control

#### 🤖 AI Model Integration
- **Gemini 2.5 Flash**: Google's latest conversational AI
- **Mistral 7B**: Advanced language model via OpenRouter
- **Context Management**: Conversation history and user preferences
- **Response Optimization**: Voice-friendly output formatting

## 🛠️ Advanced Configuration

### 🎛️ **Voice Settings**
```python
# Voice Recognition Configuration
VOICE_CONFIG = {
    "energy_threshold": 400,
    "pause_threshold": 1.2,
    "timeout": 8,
    "phrase_time_limit": 15,
    "language": "en-IN"  # or "en-US"
}
```

### 🤖 **AI Model Settings**
```python
# Gemini Configuration
GEMINI_CONFIG = {
    "model": "gemini-2.0-flash-exp",
    "temperature": 0.7,
    "max_output_tokens": 200,
    "top_p": 0.8,
    "top_k": 40
}

# Mistral Configuration
MISTRAL_CONFIG = {
    "model": "mistralai/mistral-7b-instruct:free",
    "temperature": 0.7,
    "max_tokens": 200,
    "top_p": 0.9
}
```

### 🗣️ **Text-to-Speech Settings**
```python
# TTS Configuration
TTS_CONFIG = {
    "rate": 180,        # Speech speed
    "volume": 0.9,      # Volume level
    "voice": "female"   # Voice preference
}
```

## 🚀 Deployment Options

### 🖥️ **Local Development**
```bash
# Standard execution
python main.py

# With debug logging
python main.py --debug

# Batch file (Windows)
launch_sage.bat
```

### ☁️ **Cloud Deployment**
```bash
# Docker deployment (future)
docker build -t sage-ai .
docker run -p 8501:8501 sage-ai

# Heroku deployment (future)
git push heroku main
```

### 📱 **Mobile Integration**
- **Web Interface**: Responsive design for mobile browsers
- **Voice Commands**: Mobile microphone support
- **Touch Controls**: Fallback for voice commands

## 🛠️ Troubleshooting

### 🎤 **Voice Recognition Issues**

| Problem | Solution |
|---------|----------|
| Microphone not detected | Check Windows privacy settings |
| Poor recognition accuracy | Adjust `energy_threshold` in code |
| Timeout errors | Increase timeout values |
| Background noise | Use noise cancellation headset |

### 🤖 **AI Model Issues**

| Problem | Solution |
|---------|----------|
| Gemini API errors | Verify API key and quota |
| Mistral connection failed | Check OpenRouter API key |
| Slow responses | Switch to faster model |
| Context loss | Check database permissions |

### 📧 **Email Problems**

| Problem | Solution |
|---------|----------|
| Authentication failed | Use Gmail App Password |
| SMTP errors | Check firewall settings |
| Contact not found | Update CONTACTS in config.py |
| Email not sent | Verify internet connection |

## 📊 Performance Metrics

### ⚡ **Response Times**
- **Voice Recognition**: ~1-2 seconds
- **AI Processing**: ~2-3 seconds (Gemini), ~3-5 seconds (Mistral)
- **System Commands**: ~0.5-1 seconds
- **Database Operations**: ~0.1-0.5 seconds

### 💾 **Resource Usage**
- **Memory**: ~100-200 MB during operation
- **CPU**: ~5-15% during voice processing
- **Storage**: ~50 MB + conversation history
- **Network**: Minimal (only for AI API calls)

## 🔒 Security & Privacy

### 🛡️ **Data Protection**
- **Local Storage**: All personal data stored locally
- **API Security**: Encrypted API communications
- **No Telemetry**: No usage data sent to external servers
- **Voice Privacy**: Audio not stored or transmitted

### 🔐 **Best Practices**
- Keep API keys secure and private
- Regularly update dependencies
- Use strong email passwords
- Monitor API usage and quotas

## 🤝 Contributing

### 🐛 **Bug Reports**
1. Check existing issues on GitHub
2. Provide detailed error logs
3. Include system specifications
4. Steps to reproduce the issue

### 💡 **Feature Requests**
1. Open a GitHub issue
2. Describe the feature clearly
3. Explain the use case
4. Consider implementation complexity

### 🔧 **Development Setup**
```bash
# Fork the repository
git clone https://github.com/yourusername/Sage-AI.git

# Create feature branch
git checkout -b feature/new-feature

# Make changes and test
python main.py

# Submit pull request
git push origin feature/new-feature
```

## 📄 License

This project is licensed under a **Private License**. All rights reserved.

- ✅ Personal use allowed
- ❌ Commercial use prohibited
- ❌ Redistribution prohibited
- ❌ Modification for distribution prohibited

## 🙏 Acknowledgments

### 🤖 **AI Models**
- **Google Gemini 2.5 Flash** - Advanced conversational AI
- **Mistral AI** - Open-source language model
- **OpenRouter** - AI model API gateway

### 📚 **Libraries & Tools**
- **SpeechRecognition** - Voice input processing
- **pyttsx3** - Text-to-speech synthesis
- **Rich** - Beautiful console output
- **SQLite** - Local database storage
- **Colorama** - Cross-platform colored terminal text

### 👨‍💻 **Developer**
Built with ❤️ by **Sohom** | [GitHub](https://github.com/Sagexd08)

---

<div align="center">

**🤖 Sage AI - The Future of Personal Assistants**

[![GitHub Stars](https://img.shields.io/github/stars/Sagexd08/Sage-AI?style=social)](https://github.com/Sagexd08/Sage-AI)
[![GitHub Forks](https://img.shields.io/github/forks/Sagexd08/Sage-AI?style=social)](https://github.com/Sagexd08/Sage-AI)

*"Intelligence is not about knowing everything, but about understanding what matters."*

</div>
