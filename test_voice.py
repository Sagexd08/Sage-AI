#!/usr/bin/env python3
"""
Simple test script for voice assistant functionality
"""

import pyttsx3
import speech_recognition as sr
import time

def test_tts():
    """Test text-to-speech"""
    print("Testing TTS...")
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 180)
        engine.setProperty('volume', 0.9)
        
        # Try to set a female voice
        voices = engine.getProperty('voices')
        if voices:
            for voice in voices:
                if any(keyword in voice.name.lower() for keyword in ['zira', 'female', 'woman']):
                    engine.setProperty('voice', voice.id)
                    break
        
        engine.say("Hello Sohom! Voice test is working perfectly.")
        engine.runAndWait()
        print("✓ TTS test successful!")
        return True
    except Exception as e:
        print(f"✗ TTS test failed: {e}")
        return False

def test_speech_recognition():
    """Test speech recognition"""
    print("Testing Speech Recognition...")
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            print("Say something...")
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            
        print("Processing speech...")
        text = r.recognize_google(audio, language="en-US")
        print(f"You said: {text}")
        print("✓ Speech recognition test successful!")
        return True
    except sr.WaitTimeoutError:
        print("✗ Speech recognition timeout")
        return False
    except sr.UnknownValueError:
        print("✗ Could not understand audio")
        return False
    except Exception as e:
        print(f"✗ Speech recognition test failed: {e}")
        return False

def test_ai_models():
    """Test AI model connections"""
    print("Testing AI model connections...")
    
    # Test Gemini
    try:
        import google.generativeai as genai
        from config import gemini_api_key
        
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content("Say 'Gemini test successful'")
        print(f"Gemini response: {response.text}")
        print("✓ Gemini test successful!")
    except Exception as e:
        print(f"✗ Gemini test failed: {e}")
    
    # Test OpenRouter LLM
    try:
        import requests
        from config import apikey
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {apikey}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [{"role": "user", "content": "Say 'LLM test successful'"}],
            "max_tokens": 50
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            llm_response = result['choices'][0]['message']['content']
            print(f"LLM response: {llm_response}")
            print("✓ LLM test successful!")
        else:
            print(f"✗ LLM test failed: HTTP {response.status_code}")
    except Exception as e:
        print(f"✗ LLM test failed: {e}")

def main():
    """Run all tests"""
    print("🤖 Sage AI Voice Assistant Test Suite")
    print("=" * 50)
    
    # Test TTS
    tts_ok = test_tts()
    time.sleep(1)
    
    # Test Speech Recognition
    print("\n" + "-" * 30)
    sr_ok = test_speech_recognition()
    time.sleep(1)
    
    # Test AI Models
    print("\n" + "-" * 30)
    test_ai_models()
    
    print("\n" + "=" * 50)
    if tts_ok and sr_ok:
        print("✓ Core voice functionality is working!")
        print("You can now run 'python main.py' to start the full assistant.")
    else:
        print("✗ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
