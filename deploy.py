#!/usr/bin/env python3
"""
Sage AI Deployment Script
Handles local and cloud deployment of the Streamlit app
"""

import subprocess
import sys
import os
import webbrowser
import time

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def run_voice_assistant():
    """Run Sage AI Voice Assistant"""
    print("🚀 Starting Sage AI Voice Assistant...")
    try:
        # Run voice assistant
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n👋 Sage AI Voice Assistant stopped by user")
    except Exception as e:
        print(f"❌ Error running voice assistant: {e}")

def check_dependencies():
    """Check if all dependencies are available"""
    print("🔍 Checking dependencies...")
    
    required_modules = [
        'speechrecognition',
        'pyttsx3',
        'requests',
        'numpy',
        'google.generativeai',
        'colorama',
        'rich'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - Missing")
            missing_modules.append(module)
    
    return len(missing_modules) == 0

def create_config_template():
    """Create configuration template if it doesn't exist"""
    if not os.path.exists('config.py'):
        print("📝 Creating config template...")
        config_template = '''# Sage AI Configuration
# OpenRouter API key for Mistral
apikey = "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"

# Google Gemini API key
gemini_api_key = "AIzaSyB63QId1vNy9mnF2lLWVxHOXtZ5MWKTndo"

# Email Configuration (Update with your actual email credentials)
EMAIL_CONFIG = {
    "from_email": "your_email@gmail.com",  # Replace with your Gmail address
    "password": "your_app_password",       # Replace with your Gmail app password
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587
}

# Common contacts (Add your frequently contacted emails)
CONTACTS = {
    "mom": "mom@example.com",
    "dad": "dad@example.com",
    "friend": "friend@example.com",
    "work": "work@example.com"
}
'''
        with open('config.py', 'w') as f:
            f.write(config_template)
        print("✅ Config template created! Please update config.py with your credentials.")

def main():
    """Main deployment function"""
    print("🤖 Sage AI Deployment Manager")
    print("=" * 50)
    
    # Create config if needed
    create_config_template()
    
    # Check dependencies
    if not check_dependencies():
        print("\n📦 Installing missing dependencies...")
        if not install_requirements():
            print("❌ Failed to install requirements. Please install manually.")
            return
    
    print("\n🎯 Choose deployment option:")
    print("1. Run Sage Voice Assistant (recommended)")
    print("2. Install requirements only")
    print("3. Exit")

    choice = input("\nEnter your choice (1-3): ").strip()

    if choice == "1":
        print("\n🚀 Starting Sage Voice Assistant...")
        time.sleep(1)
        run_voice_assistant()
    elif choice == "2":
        install_requirements()
        print("✅ Requirements installed. Run 'python main.py' to start the voice assistant.")
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main()
