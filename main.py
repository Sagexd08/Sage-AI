import speech_recognition as sr
import os
import webbrowser
import requests
import json
import pyttsx3
from config import apikey, gemini_api_key, EMAIL_CONFIG, CONTACTS
import datetime
import random
import numpy as np
import smtplib
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import urllib.parse
import time
import threading
import queue
import logging
from typing import Dict, List, Tuple, Optional
import asyncio
import re
import psutil
import pyautogui
import schedule
import pickle
import sqlite3
from pathlib import Path
import cv2
import winreg
import winsound
import socket
import platform
import speedtest
import geocoder
import wikipedia
import yfinance as yf
import google.generativeai as genai
from colorama import init, Fore, Back, Style
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Initialize colorama and rich console
init(autoreset=True)
console = Console()


# Global variables
chatStr = ""
tts_engine = None
is_speaking = False
should_stop_speaking = False
conversation_active = False
last_interaction_time = None
continuous_listening = False
sage_instance = None  # Global reference to sage instance for legacy functions

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sage.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize TTS engine
try:
    tts_engine = pyttsx3.init()
    voices = tts_engine.getProperty('voices')
    if voices:
        for voice in voices:
            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                tts_engine.setProperty('voice', voice.id)
                break
    tts_engine.setProperty('rate', 180)
    tts_engine.setProperty('volume', 0.9)
except Exception as e:
    print(f"TTS setup error: {e}")

class AdvancedSageAI:
    """Sage AI Assistant"""

    def __init__(self):
        self.chat_history = []
        self.user_preferences = {}
        self.reminders = []
        self.is_listening = False
        self.conversation_context = []
        self.command_history = []
        self.wake_words = ["sage", "hey sage", "ok sage", "jarvis"]
        self.exit_words = ["goodbye", "bye", "exit", "quit", "stop", "shutdown"]
        self.user_name = "Sohom"
        self.assistant_name = "Sage"
        self.continuous_mode = False
        self.preferred_ai = None  # Will be set by user choice
        self.ai_models = {
            "gemini": "Gemini 2.5 Flash",
            "llm": "Mistral LLM via OpenRouter"
        }
        self.initialize_components()
        self.load_user_data()

    def initialize_components(self):
        """Initialize all AI components including Gemini"""
        try:
            # Initialize Gemini AI
            self.initialize_gemini()

            # Initialize TTS
            self.tts_engine = pyttsx3.init()
            self.setup_voice()

            # Initialize database
            self.init_database()

            # Initialize scheduler
            self.scheduler = schedule

            # Display startup message
            console.print(Panel.fit(
                f"[bold green]{self.assistant_name} AI Assistant Initialized[/bold green]\n"
                f"[cyan]Ready to assist {self.user_name}![/cyan]\n"
                f"[yellow]Say '{self.wake_words[0]}' to activate[/yellow]",
                border_style="green"
            ))

            logger.info("Sage AI components initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            console.print(f"[red]Initialization error: {e}[/red]")

    def initialize_gemini(self):
        """Initialize Google Gemini 2.5 AI"""
        try:
            genai.configure(api_key=gemini_api_key)
            # Use Gemini 2.5 Flash model for better performance and capabilities
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')

            # Configure generation settings for voice assistant
            self.generation_config = genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.8,
                top_k=40,
                max_output_tokens=200,  # Keep responses concise for voice
                response_mime_type="text/plain"
            )

            # Test the connection
            test_response = self.gemini_model.generate_content(
                "Hello, respond with just 'Connected'",
                generation_config=self.generation_config
            )
            logger.info("Gemini 2.5 AI initialized successfully")
            console.print("[green]✓ Gemini 2.5 Flash connected[/green]")

        except Exception as e:
            logger.error(f"Gemini initialization error: {e}")
            console.print(f"[red]✗ Gemini 2.5 connection failed: {e}[/red]")
            # Fallback to older model if 2.5 is not available
            try:
                self.gemini_model = genai.GenerativeModel('gemini-pro')
                self.generation_config = genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=200
                )
                console.print("[yellow]⚠ Using Gemini Pro as fallback[/yellow]")
            except:
                self.gemini_model = None

    def ask_ai_preference(self):
        """Ask user which AI model they prefer to use"""
        try:
            console.print("\n[bold yellow]🤖 AI Model Selection[/bold yellow]")
            self.say("Hello! Before we start, I need to know which AI model you'd like me to use.")
            time.sleep(1.5)

            console.print("[cyan]Option 1: Gemini 2.5 Flash[/cyan] - Google's latest AI model")
            self.say("Option 1: Gemini 2.5 Flash - Google's latest AI model, great for conversations and general tasks.")
            time.sleep(2)

            console.print("[cyan]Option 2: Mistral LLM[/cyan] - Powerful language model via OpenRouter")
            self.say("Option 2: Mistral LLM - Powerful language model via OpenRouter, excellent for detailed responses.")
            time.sleep(2)

            console.print("[bold green]Please say 'Gemini' or 'LLM' to choose:[/bold green]")
            self.say("Which would you prefer? Say 'Gemini' for option 1, or 'LLM' for option 2.")

            # Listen for preference
            for attempt in range(3):  # Give user 3 attempts
                preference = self.listen_for_command(timeout=15)

                if "gemini" in preference.lower():
                    self.preferred_ai = "gemini"
                    console.print(f"[green]✓ Selected: {self.ai_models['gemini']}[/green]")
                    self.say(f"Perfect! I'll use {self.ai_models['gemini']} for our conversations. This model is excellent for natural conversations.")
                    self.save_user_preference("preferred_ai", "gemini")
                    return True
                elif "llm" in preference.lower() or "mistral" in preference.lower():
                    self.preferred_ai = "llm"
                    console.print(f"[green]✓ Selected: {self.ai_models['llm']}[/green]")
                    self.say(f"Excellent choice! I'll use {self.ai_models['llm']} for our conversations. This model provides detailed and thoughtful responses.")
                    self.save_user_preference("preferred_ai", "llm")
                    return True
                elif preference in ["timeout", "unknown", "error"]:
                    if attempt < 2:
                        self.say("I didn't catch that. Please say 'Gemini' or 'LLM'.")
                    continue
                else:
                    if attempt < 2:
                        self.say("Please choose either 'Gemini' or 'LLM'.")

            # Default to Gemini if no clear choice
            self.preferred_ai = "gemini"
            self.say("I'll default to using Gemini 2.5 Flash. You can change this anytime by saying 'change AI model'.")
            self.save_user_preference("preferred_ai", "gemini")
            return True

        except Exception as e:
            logger.error(f"AI preference selection error: {e}")
            self.preferred_ai = "gemini"  # Default fallback
            return False

    def chat_with_llm(self, user_input: str) -> str:
        """Chat using Mistral LLM via OpenRouter"""
        try:
            # OpenRouter API endpoint
            url = "https://openrouter.ai/api/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {apikey}",
                "Content-Type": "application/json"
            }

            # Build conversation context
            messages = [
                {
                    "role": "system",
                    "content": f"You are {self.assistant_name}, an advanced AI voice assistant for {self.user_name}. You are helpful, intelligent, conversational, and have a friendly personality. Keep responses concise but informative for voice interaction (1-3 sentences max). Address {self.user_name} by name occasionally."
                }
            ]

            # Add recent conversation history
            for exchange in self.chat_history[-3:]:
                if 'user' in exchange and 'assistant' in exchange:
                    messages.append({"role": "user", "content": exchange['user']})
                    messages.append({"role": "assistant", "content": exchange['assistant']})

            # Add current query
            messages.append({"role": "user", "content": user_input})

            data = {
                "model": "mistralai/mistral-7b-instruct:free",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 200,
                "top_p": 0.9,
                "frequency_penalty": 0.1,
                "presence_penalty": 0.1
            }

            response = requests.post(url, headers=headers, json=data, timeout=30)

            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content'].strip()

                # Store conversation
                self.chat_history.append({
                    "user": user_input,
                    "assistant": ai_response,
                    "timestamp": datetime.datetime.now().isoformat()
                })

                # Keep only last 10 conversations
                if len(self.chat_history) > 10:
                    self.chat_history = self.chat_history[-10:]

                return ai_response
            else:
                return "I'm having trouble connecting to my LLM brain right now."

        except Exception as e:
            logger.error(f"LLM chat error: {e}")
            return "I'm having trouble processing that with the LLM right now."

    def get_ai_response(self, user_input: str) -> str:
        """Get AI response based on user's preferred model"""
        if self.preferred_ai == "llm":
            return self.chat_with_llm(user_input)
        else:  # Default to Gemini
            return self.chat_with_gemini(user_input)

    def setup_voice(self):
        """Setup advanced voice configuration"""
        try:
            voices = self.tts_engine.getProperty('voices')

            # Try to find a female voice
            for voice in voices:
                if any(keyword in voice.name.lower() for keyword in ['zira', 'female', 'woman']):
                    self.tts_engine.setProperty('voice', voice.id)
                    break

            # Voice settings
            self.tts_engine.setProperty('rate', 180)  # Speed
            self.tts_engine.setProperty('volume', 0.9)  # Volume

        except Exception as e:
            logger.error(f"Voice setup error: {e}")

    def init_database(self):
        """Initialize SQLite database for storing user data"""
        try:
            self.db_path = Path("sage_data.db")
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            cursor = self.conn.cursor()

            # Create tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    user_input TEXT,
                    sage_response TEXT,
                    context TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reminder_text TEXT,
                    reminder_time TEXT,
                    is_completed BOOLEAN DEFAULT FALSE,
                    created_at TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_preferences (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            ''')

            self.conn.commit()
            logger.info("Database initialized successfully")

        except Exception as e:
            logger.error(f"Database initialization error: {e}")

    def save_conversation(self, user_input: str, sage_response: str, context: str = ""):
        """Save conversation to database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO conversations (timestamp, user_input, sage_response, context)
                VALUES (?, ?, ?, ?)
            ''', (datetime.datetime.now().isoformat(), user_input, sage_response, context))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")

    def load_user_data(self):
        """Load user preferences and data"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT key, value FROM user_preferences')
            preferences = cursor.fetchall()

            for key, value in preferences:
                try:
                    self.user_preferences[key] = json.loads(value)
                except:
                    self.user_preferences[key] = value

            logger.info("User data loaded successfully")

        except Exception as e:
            logger.error(f"Error loading user data: {e}")

    def save_user_preference(self, key: str, value):
        """Save user preference to database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO user_preferences (key, value)
                VALUES (?, ?)
            ''', (key, json.dumps(value) if isinstance(value, (dict, list)) else str(value)))
            self.conn.commit()
            self.user_preferences[key] = value
        except Exception as e:
            logger.error(f"Error saving preference: {e}")

    def say(self, text: str, interrupt: bool = False):
        """Simplified and reliable text-to-speech"""
        try:
            if interrupt:
                try:
                    self.tts_engine.stop()
                except:
                    pass

            # Add personality to responses
            if "sohom" not in text.lower() and random.random() < 0.3:
                text = f"Sohom, {text}"

            # Display what Sage is saying
            console.print(f"[bold cyan]🤖 {self.assistant_name}:[/bold cyan] [white]{text}[/white]")

            # Use direct TTS without threading to avoid conflicts
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                # Fallback: create new engine instance
                try:
                    fallback_tts = pyttsx3.init()
                    fallback_tts.setProperty('rate', 180)
                    fallback_tts.setProperty('volume', 0.9)
                    fallback_tts.say(text)
                    fallback_tts.runAndWait()
                except Exception as e2:
                    logger.error(f"TTS fallback error: {e2}")
                    console.print(f"[red]Voice output failed: {e2}[/red]")

            logger.info(f"Sage speaking: {text}")

        except Exception as e:
            logger.error(f"TTS error: {e}")
            console.print(f"[red]TTS Error: {e}[/red]")

    def process_voice_command(self, command: str) -> bool:
        """Process voice commands with enhanced intent recognition"""
        command = command.lower().strip()

        if not command or command in ["unknown", "timeout", "error"]:
            if command == "timeout":
                return True  # Continue listening
            elif command == "unknown":
                self.say("I didn't catch that. Could you repeat?")
            elif command == "error":
                self.say("I'm having trouble hearing you. Please try again.")
            return True

        # Check for exit commands
        if any(exit_word in command for exit_word in self.exit_words):
            self.say(f"Goodbye {self.user_name}! Have a great day!")
            return False

        # Check for continuous mode toggle
        if "continuous mode" in command:
            if "enable" in command or "start" in command or "on" in command:
                self.continuous_mode = True
                self.say("Continuous mode enabled. I'll keep listening.")
            elif "disable" in command or "stop" in command or "off" in command:
                self.continuous_mode = False
                self.say("Continuous mode disabled.")
            return True

        # Check for AI model change request
        if "change ai" in command or "switch ai" in command or "change model" in command:
            self.ask_ai_preference()
            return True

        # Check for AI model status request
        if "which ai" in command or "current ai" in command or "ai model" in command:
            current_model = self.ai_models.get(self.preferred_ai, "Unknown")
            self.say(f"I'm currently using {current_model}. Say 'change AI model' if you'd like to switch.")
            return True

        # Use existing command processing or chat with preferred AI
        if self.handle_existing_commands(command):
            return True
        else:
            # Use preferred AI for general conversation
            response = self.get_ai_response(command)
            self.say(response)
            return True

    def handle_existing_commands(self, command: str) -> bool:
        """Check if command matches existing functionality"""
        # Camera commands
        if any(word in command for word in ["camera", "take photo", "open camera", "activate camera"]):
            return self.handle_camera_command(command)

        # Direct website/app opening (no "open" required)
        if any(word in command for word in ["google", "youtube", "spotify", "gmail", "facebook",
                                           "twitter", "instagram", "linkedin", "reddit", "netflix"]):
            return self.handle_web_command(command)

        # Music commands
        if any(word in command for word in ["play", "music", "song"]):
            return self.handle_music_command(command)

        # Email commands
        if any(word in command for word in ["email", "send", "mail"]):
            return self.handle_email_command(command)

        # App commands
        if any(word in command for word in ["open", "launch", "start"]):
            return self.handle_app_command(command)

        # Web commands and search
        if any(word in command for word in ["website", "search"]):
            return self.handle_web_command(command)

        # Time command
        if "time" in command:
            return self.handle_time_command()

        return False  # Command not handled, use AI chat

    def handle_music_command(self, command: str) -> bool:
        """Handle music-related commands"""
        try:
            song_name = ""
            service = "spotify"  # default

            # Extract service preference
            if "spotify" in command:
                service = "spotify"
            elif "youtube" in command:
                service = "youtube"
            elif "apple" in command:
                service = "apple"

            # Extract song name
            if "play" in command:
                parts = command.split("play")
                if len(parts) > 1:
                    song_part = parts[1].strip()
                    # Remove service name from song
                    for svc in ["on spotify", "on youtube", "on apple music", "spotify", "youtube"]:
                        song_part = song_part.replace(svc, "").strip()
                    song_name = song_part

            # Use existing music functions
            if service == "spotify":
                play_music_on_spotify(song_name)
            elif service == "youtube":
                play_music_on_youtube(song_name)
            elif service == "apple":
                play_music_on_apple_music(song_name)

            return True

        except Exception as e:
            logger.error(f"Music command error: {e}")
            self.say("I had trouble with that music command.")
            return True

    def handle_app_command(self, command: str) -> bool:
        """Handle application opening commands"""
        try:
            # Define applications and their commands
            apps = {
                "notepad": "notepad",
                "calculator": "calc",
                "paint": "mspaint",
                "chrome": "chrome",
                "firefox": "firefox",
                "edge": "msedge",
                "explorer": "explorer",
                "file explorer": "explorer",
                "cmd": "cmd",
                "command prompt": "cmd",
                "powershell": "powershell",
                "word": "winword",
                "excel": "excel",
                "powerpoint": "powerpnt",
                "outlook": "outlook",
                "teams": "ms-teams:",
                "settings": "ms-settings:",
                "store": "ms-windows-store:",
                "control panel": "control",
                "task manager": "taskmgr",
                "camera": "start microsoft.windows.camera:",
                "photos": "ms-photos:",
                "mail": "ms-mail:",
                "calendar": "ms-calendar:",
                "maps": "bingmaps:",
                "weather": "bingweather:",
                "news": "bingnews:",
                "music": "mswindowsmusic:",
                "movies": "ms-xboxliveapp-1297287741:",
                "xbox": "ms-xboxliveapp-1297287741:"
            }

            # Find which app to open
            for app_name, app_command in apps.items():
                if app_name in command.lower():
                    try:
                        # Handle Windows Store apps and special protocols
                        if app_name in ["teams", "settings", "store", "camera", "photos", "mail",
                                       "calendar", "maps", "weather", "news", "music", "movies", "xbox"]:
                            os.system(f"start {app_command}")
                            if app_name == "camera":
                                self.say("Opening camera application")
                            else:
                                self.say(f"Opening {app_name}")
                        else:
                            subprocess.Popen(app_command, shell=True)
                            self.say(f"Opening {app_name}")
                        return True
                    except Exception as e:
                        logger.error(f"App opening error: {e}")
                        self.say(f"I couldn't open {app_name}")
                        return True

            # If no specific app found, try generic open command
            if "open" in command:
                # Extract what to open
                parts = command.split("open")
                if len(parts) > 1:
                    app_to_open = parts[1].strip()
                    if app_to_open:
                        try:
                            subprocess.Popen(app_to_open, shell=True)
                            self.say(f"Trying to open {app_to_open}")
                            return True
                        except:
                            self.say(f"I couldn't find or open {app_to_open}")
                            return True

            self.say("I'm not sure which application you want to open.")
            return True

        except Exception as e:
            logger.error(f"App command error: {e}")
            self.say("I had trouble with that application command.")
            return True

    def handle_web_command(self, command: str) -> bool:
        """Handle web-related commands"""
        try:
            # Common websites - now includes Spotify web
            websites = {
                "google": "https://www.google.com",
                "youtube": "https://www.youtube.com",
                "spotify": "https://open.spotify.com",
                "gmail": "https://mail.google.com",
                "github": "https://www.github.com",
                "facebook": "https://www.facebook.com",
                "twitter": "https://www.twitter.com",
                "instagram": "https://www.instagram.com",
                "linkedin": "https://www.linkedin.com",
                "reddit": "https://www.reddit.com",
                "stackoverflow": "https://stackoverflow.com",
                "wikipedia": "https://www.wikipedia.org",
                "netflix": "https://www.netflix.com",
                "amazon": "https://www.amazon.com",
                "whatsapp": "https://web.whatsapp.com"
            }

            # Check for specific websites
            for site_name, url in websites.items():
                if site_name in command.lower():
                    webbrowser.open(url)
                    self.say(f"Opening {site_name}")
                    return True

            # Handle search queries
            if "search" in command:
                # Extract search query
                parts = command.split("search")
                if len(parts) > 1:
                    search_query = parts[1].strip()
                    if "for" in search_query:
                        search_query = search_query.split("for")[1].strip()

                    if search_query:
                        search_url = f"https://www.google.com/search?q={urllib.parse.quote(search_query)}"
                        webbrowser.open(search_url)
                        self.say(f"Searching for {search_query}")
                        return True

            return False

        except Exception as e:
            logger.error(f"Web command error: {e}")
            self.say("I had trouble with that web command.")
            return True

    def handle_email_command(self, command: str) -> bool:
        """Handle email-related commands"""
        try:
            # Check if contact name is mentioned
            recipient = None
            for contact_name, email in CONTACTS.items():
                if contact_name in command:
                    recipient = email
                    break

            if not recipient:
                self.say("Who would you like to send the email to? Please mention a contact name.")
                return True

            # For now, send a simple email
            subject = "Message from Sohom via Sage AI"
            body = "Hi,\n\nThis is a message sent through my AI assistant Sage.\n\nBest regards,\nSohom"

            if send_email(recipient, subject, body):
                self.say("Email sent successfully!")
            else:
                self.say("I couldn't send the email. Please check your email configuration.")

            return True

        except Exception as e:
            logger.error(f"Email command error: {e}")
            self.say("I had trouble with that email command.")
            return True

    def handle_time_command(self) -> bool:
        """Handle time-related commands"""
        try:
            now = datetime.datetime.now()
            hour = now.strftime("%I")  # 12-hour format
            minute = now.strftime("%M")
            am_pm = now.strftime("%p")

            self.say(f"The time is {hour}:{minute} {am_pm}")
            return True

        except Exception as e:
            logger.error(f"Time command error: {e}")
            self.say("I had trouble getting the time.")
            return True

    def handle_camera_command(self, command: str) -> bool:
        """Handle camera-related commands with multiple fallback options"""
        try:
            self.say("Opening camera")

            # Try multiple methods to open camera
            camera_opened = False

            # Method 1: Windows Camera app
            try:
                os.system("start microsoft.windows.camera:")
                camera_opened = True
                self.say("Camera application opened")
            except:
                pass

            # Method 2: If Windows Camera fails, try alternative
            if not camera_opened:
                try:
                    subprocess.Popen("start ms-camera:", shell=True)
                    camera_opened = True
                    self.say("Camera opened successfully")
                except:
                    pass

            # Method 3: Try opening via explorer
            if not camera_opened:
                try:
                    os.system("explorer.exe shell:AppsFolder\\Microsoft.WindowsCamera_8wekyb3d8bbwe!App")
                    camera_opened = True
                    self.say("Camera launched")
                except:
                    pass

            # Method 4: Last resort - try generic camera command
            if not camera_opened:
                try:
                    os.system("start camera")
                    self.say("Attempting to open camera")
                    camera_opened = True
                except:
                    pass

            if not camera_opened:
                self.say("I couldn't open the camera. Please check if the camera app is installed.")

            return True

        except Exception as e:
            logger.error(f"Camera command error: {e}")
            self.say("I had trouble opening the camera.")
            return True

    def listen_for_command(self, timeout: int = 8, wake_word_mode: bool = False) -> str:
        """Advanced voice recognition with noise filtering and wake word detection"""
        r = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                if not wake_word_mode:
                    console.print("[yellow]🎤 Adjusting for ambient noise...[/yellow]")
                    r.adjust_for_ambient_noise(source, duration=1.5)

                r.pause_threshold = 1.2
                r.energy_threshold = 400
                r.dynamic_energy_threshold = True

                if wake_word_mode:
                    console.print(f"[cyan]👂 Listening for wake word ({', '.join(self.wake_words)})...[/cyan]")
                else:
                    console.print("[yellow]🎧 Listening...[/yellow]")

                audio = r.listen(source, timeout=timeout, phrase_time_limit=15)

                console.print("[yellow]🧠 Processing speech...[/yellow]")

                # Try multiple recognition engines
                try:
                    query = r.recognize_google(audio, language="en-in")
                    logger.info(f"Voice command recognized: {query}")
                    result = query.lower().strip()

                    if not wake_word_mode:
                        console.print(f"[bold green]👤 {self.user_name}:[/bold green] [white]{query}[/white]")

                    return result
                except:
                    # Fallback to different language model
                    try:
                        query = r.recognize_google(audio, language="en-us")
                        logger.info(f"Voice command recognized (fallback): {query}")
                        result = query.lower().strip()

                        if not wake_word_mode:
                            console.print(f"[bold green]👤 {self.user_name}:[/bold green] [white]{query}[/white]")

                        return result
                    except:
                        return "unknown"

        except sr.WaitTimeoutError:
            if not wake_word_mode:
                logger.warning("Voice recognition timeout")
            return "timeout"
        except sr.UnknownValueError:
            if not wake_word_mode:
                logger.warning("Could not understand audio")
            return "unknown"
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return "error"
        except Exception as e:
            logger.error(f"Listening error: {e}")
            return "error"

    def chat_with_gemini(self, user_input: str) -> str:
        """Enhanced chat with Gemini 2.5 using conversation context and advanced features"""
        if not self.gemini_model:
            return "I'm sorry, my AI brain is not available right now."

        try:
            # Build conversation context with system instructions
            system_instruction = f"""You are {self.assistant_name}, an advanced AI voice assistant for {self.user_name}.

            Personality traits:
            - Helpful, intelligent, and conversational
            - Friendly but professional
            - Concise responses perfect for voice interaction (1-2 sentences max)
            - Occasionally address {self.user_name} by name
            - Show personality and warmth in responses

            Context: This is a voice conversation, so keep responses natural and spoken-friendly.
            """

            # Prepare conversation history for context
            conversation_context = ""
            for exchange in self.chat_history[-3:]:
                if 'user' in exchange and 'assistant' in exchange:
                    conversation_context += f"{self.user_name}: {exchange['user']}\n{self.assistant_name}: {exchange['assistant']}\n"

            # Create the full prompt
            full_prompt = f"{system_instruction}\n\nRecent conversation:\n{conversation_context}\n\nCurrent request: {user_input}\n\nRespond as {self.assistant_name}:"

            # Generate response with Gemini 2.5
            response = self.gemini_model.generate_content(
                full_prompt,
                generation_config=self.generation_config
            )

            ai_response = response.text.strip()

            # Clean up response for voice output
            ai_response = ai_response.replace("*", "").replace("#", "").strip()

            # Store conversation
            self.chat_history.append({
                "user": user_input,
                "assistant": ai_response,
                "timestamp": datetime.datetime.now().isoformat()
            })

            # Keep only last 10 conversations to manage memory
            if len(self.chat_history) > 10:
                self.chat_history = self.chat_history[-10:]

            return ai_response

        except Exception as e:
            logger.error(f"Gemini 2.5 chat error: {e}")
            return "I'm having trouble processing that right now. Could you try again?"

# Enhanced chat function using user's preferred AI model
def chat(query, preferred_ai="gemini"):
    global chatStr
    console.print(f"[dim]{chatStr}[/dim]")
    chatStr += f"Sohom: {query}\n Sage: "

    try:
        if preferred_ai == "llm":
            # Use Mistral LLM via OpenRouter
            url = "https://openrouter.ai/api/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {apikey}",
                "Content-Type": "application/json"
            }

            enhanced_prompt = f"""You are Sage, an advanced AI voice assistant for Sohom.
            You are helpful, intelligent, conversational, and have a friendly personality.
            Keep responses concise but informative for voice interaction (1-2 sentences).
            Address Sohom by name occasionally.

            Conversation history:
            {chatStr}

            Current query: {query}

            Respond as Sage:"""

            data = {
                "model": "mistralai/mistral-7b-instruct:free",
                "messages": [
                    {"role": "system", "content": "You are Sage, a helpful AI voice assistant for Sohom."},
                    {"role": "user", "content": enhanced_prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 150,
                "top_p": 0.9
            }

            response = requests.post(url, headers=headers, json=data, timeout=30)

            if response.status_code == 200:
                result = response.json()
                response_text = result['choices'][0]['message']['content'].strip()
            else:
                response_text = "I'm having trouble with my LLM connection right now."

        else:
            # Use Gemini 2.5 (default)
            genai.configure(api_key=gemini_api_key)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')

            # Configure generation for voice interaction
            generation_config = genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.8,
                top_k=40,
                max_output_tokens=150,
                response_mime_type="text/plain"
            )

            enhanced_prompt = f"""You are Sage, an advanced AI voice assistant for Sohom.

            Personality:
            - Helpful, intelligent, and conversational
            - Friendly but professional tone
            - Keep responses concise for voice interaction (1-2 sentences max)
            - Address Sohom by name occasionally
            - Show warmth and personality

            Conversation history:
            {chatStr}

            Current query: {query}

            Respond as Sage in a natural, conversational way:"""

            # Generate response with Gemini 2.5
            response = model.generate_content(
                enhanced_prompt,
                generation_config=generation_config
            )
            response_text = response.text.strip()

        # Clean up response for voice output
        response_text = response_text.replace("*", "").replace("#", "").strip()

        # Display and speak response
        console.print(f"[bold cyan]🤖 Sage:[/bold cyan] [white]{response_text}[/white]")
        say(response_text)
        chatStr += f"{response_text}\n"
        return response_text

    except Exception as e:
        error_msg = "I'm having trouble processing that right now."
        console.print(f"[red]Error: {str(e)}[/red]")
        say(error_msg)
        return error_msg


def ai(prompt):
    try:
        text = f"Mistral AI response for Prompt: {prompt} \n *************************\n\n"

        # OpenRouter API endpoint
        url = "https://openrouter.ai/api/v1/chat/completions"

        # Headers for OpenRouter API
        headers = {
            "Authorization": f"Bearer {apikey}",
            "Content-Type": "application/json"
        }

        # Request payload for Mistral model
        data = {
            "model": "mistralai/devstral-small:free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 256,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }

        # Make the API request
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            response_text = result['choices'][0]['message']['content']
            text += response_text

            if not os.path.exists("Openai"):
                os.mkdir("Openai")

            # Create filename from prompt
            filename = ''.join(prompt.split('intelligence')[1:]).strip() if 'intelligence' in prompt else f"prompt-{random.randint(1, 2343434356)}"
            filename = filename[:50] if filename else f"prompt-{random.randint(1, 2343434356)}"  # Limit filename length

            with open(f"Openai/{filename}.txt", "w", encoding="utf-8") as f:
                f.write(text)

            print(f"Response saved to Openai/{filename}.txt")
        else:
            print(f"API Error: {response.status_code}")

    except Exception as e:
        print(f"Error in AI function: {str(e)}")

def send_email(to_email, subject, body):
    """Send email using Gmail SMTP"""
    try:
        # Use email config from config.py
        from_email = EMAIL_CONFIG["from_email"]
        password = EMAIL_CONFIG["password"]

        # Create message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Add body to email
        msg.attach(MIMEText(body, 'plain'))

        # Gmail SMTP configuration
        server = smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"])
        server.starttls()  # Enable security
        server.login(from_email, password)

        # Send email
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()

        say(f"Email sent successfully to {to_email}")
        print(f"Email sent to {to_email}")
        return True

    except Exception as e:
        say("Sorry, I couldn't send the email. Please check your email configuration.")
        print(f"Email error: {str(e)}")
        return False

def get_contact_email(contact_name):
    """Get email address from contacts"""
    contact_name = contact_name.lower()
    if contact_name in CONTACTS:
        return CONTACTS[contact_name]
    return None

def play_music_on_spotify(song_name="", artist_name=""):
    """Play music on Spotify"""
    try:
        if song_name:
            # Create search query
            if artist_name:
                search_query = f"{song_name} {artist_name}"
            else:
                search_query = song_name

            # URL encode the search query
            encoded_query = urllib.parse.quote(search_query)

            # Spotify search URL
            spotify_url = f"https://open.spotify.com/search/{encoded_query}"

            # Try to open Spotify app first, then web
            try:
                # Try to open in Spotify app
                os.system(f'start spotify:search:{encoded_query}')
                say(f"Playing {song_name} on Spotify")
            except:
                # Fallback to web version
                webbrowser.open(spotify_url)
                say(f"Opening {song_name} on Spotify web")
        else:
            # Open Spotify without specific song
            try:
                os.system('start spotify:')
                say("Opening Spotify")
            except:
                webbrowser.open("https://open.spotify.com")
                say("Opening Spotify web")
        return True
    except Exception as e:
        say("Sorry, I couldn't open Spotify")
        print(f"Spotify error: {str(e)}")
        return False

def play_music_on_youtube(song_name="", artist_name=""):
    """Play music on YouTube Music"""
    try:
        if song_name:
            # Create search query
            if artist_name:
                search_query = f"{song_name} {artist_name}"
            else:
                search_query = song_name

            # URL encode the search query
            encoded_query = urllib.parse.quote(search_query)

            # YouTube Music search URL
            yt_music_url = f"https://music.youtube.com/search?q={encoded_query}"

            webbrowser.open(yt_music_url)
            say(f"Playing {song_name} on YouTube Music")
        else:
            # Open YouTube Music without specific song
            webbrowser.open("https://music.youtube.com")
            say("Opening YouTube Music")
        return True
    except Exception as e:
        say("Sorry, I couldn't open YouTube Music")
        print(f"YouTube Music error: {str(e)}")
        return False

def play_music_on_apple_music(song_name="", artist_name=""):
    """Play music on Apple Music"""
    try:
        if song_name:
            # Create search query
            if artist_name:
                search_query = f"{song_name} {artist_name}"
            else:
                search_query = song_name

            # URL encode the search query
            encoded_query = urllib.parse.quote(search_query)

            # Apple Music search URL
            apple_music_url = f"https://music.apple.com/search?term={encoded_query}"

            webbrowser.open(apple_music_url)
            say(f"Playing {song_name} on Apple Music")
        else:
            # Open Apple Music without specific song
            webbrowser.open("https://music.apple.com")
            say("Opening Apple Music")
        return True
    except Exception as e:
        say("Sorry, I couldn't open Apple Music")
        print(f"Apple Music error: {str(e)}")
        return False

def play_music_generic(song_name="", artist_name="", service="spotify"):
    """Play music on specified service"""
    service = service.lower()

    if "spotify" in service:
        return play_music_on_spotify(song_name, artist_name)
    elif "youtube" in service or "yt" in service:
        return play_music_on_youtube(song_name, artist_name)
    elif "apple" in service:
        return play_music_on_apple_music(song_name, artist_name)
    else:
        # Default to Spotify
        return play_music_on_spotify(song_name, artist_name)

def craft_email_with_ai(recipient, purpose, additional_details=""):
    """Use AI to craft an email"""
    try:
        # Create a prompt for the AI to write an email
        prompt = f"""Write a professional email for the following:

Recipient: {recipient}
Purpose: {purpose}
Additional details: {additional_details}

Please write a complete email with:
- Appropriate subject line
- Professional greeting
- Clear and concise body
- Professional closing
- Sender signature as "Sohom"

Format the response as:
Subject: [subject line]
Body: [email body]
"""

        # OpenRouter API endpoint
        url = "https://openrouter.ai/api/v1/chat/completions"

        # Headers for OpenRouter API
        headers = {
            "Authorization": f"Bearer {apikey}",
            "Content-Type": "application/json"
        }

        # Request payload for Mistral model
        data = {
            "model": "mistralai/devstral-small:free",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a professional email writing assistant. Write clear, concise, and professional emails."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 512,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }

        # Make the API request
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            email_content = result['choices'][0]['message']['content']

            # Parse the email content to extract subject and body
            lines = email_content.split('\n')
            subject = ""
            body = ""

            for i, line in enumerate(lines):
                if line.startswith("Subject:"):
                    subject = line.replace("Subject:", "").strip()
                elif line.startswith("Body:"):
                    body = '\n'.join(lines[i+1:]).strip()
                    break

            # If parsing failed, use the entire content as body
            if not subject or not body:
                subject = f"Message from Sohom"
                body = email_content

            return subject, body
        else:
            return "Message from Sohom", f"Hi,\n\n{purpose}\n\n{additional_details}\n\nBest regards,\nSohom"

    except Exception as e:
        print(f"Email crafting error: {str(e)}")
        return "Message from Sohom", f"Hi,\n\n{purpose}\n\n{additional_details}\n\nBest regards,\nSohom"

def send_crafted_email(recipient_name, purpose, additional_details=""):
    """Craft and send an email using AI"""
    try:
        # Get recipient email
        to_email = get_contact_email(recipient_name)
        if not to_email:
            say(f"I don't have {recipient_name}'s email address in my contacts.")
            return False

        say("Let me craft an email for you...")

        # Craft the email using AI
        subject, body = craft_email_with_ai(recipient_name, purpose, additional_details)

        # Send the email
        success = send_email(to_email, subject, body)

        if success:
            say(f"Email successfully crafted and sent to {recipient_name}")
            print(f"Subject: {subject}")
            print(f"Body: {body}")

        return success

    except Exception as e:
        say("Sorry, I encountered an error while crafting and sending the email.")
        print(f"Crafted email error: {str(e)}")
        return False

# ==================== ADVANCED JARVIS FUNCTIONS ====================

def jarvis_camera_control(action="open"):
    """Advanced camera control like JARVIS"""
    try:
        if action == "open" or action == "activate":
            # Try to open camera app
            os.system("start microsoft.windows.camera:")
            say("Camera activated, Mr. Sohom. Visual systems online.")
            return True
        elif action == "capture" or action == "photo":
            # Capture photo using OpenCV
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"jarvis_capture_{timestamp}.jpg"
                    cv2.imwrite(filename, frame)
                    say(f"Photo captured and saved as {filename}, sir.")
                cap.release()
                return True
            else:
                say("Unable to access camera systems, sir.")
                return False
        elif action == "scan" or action == "analyze":
            say("Initiating visual analysis protocol, sir.")
            # Advanced camera analysis would go here
            return True
    except Exception as e:
        say("Camera systems are offline, sir.")
        print(f"Camera error: {e}")
        return False

def jarvis_play_specific_song(song_name, artist="", platform="youtube"):
    """Play specific songs like JARVIS with advanced search and auto-play"""
    try:
        search_query = f"{song_name} {artist}".strip()
        encoded_query = urllib.parse.quote(search_query)

        if platform.lower() == "youtube":
            # Direct YouTube Music search for better music experience
            youtube_music_url = f"https://music.youtube.com/search?q={encoded_query}"
            webbrowser.open(youtube_music_url)

            # Wait for page to load then auto-click first result
            def auto_play_youtube():
                time.sleep(4)  # Wait for page load
                try:
                    # Try multiple click positions for first song
                    click_positions = [
                        (400, 350),  # First result position
                        (350, 300),  # Alternative position
                        (450, 400),  # Another alternative
                    ]

                    for pos in click_positions:
                        try:
                            pyautogui.click(pos[0], pos[1])
                            time.sleep(1)
                            break
                        except:
                            continue

                    # Try pressing Enter as backup
                    pyautogui.press('enter')

                except Exception as e:
                    print(f"Auto-play error: {e}")

            # Run auto-play in background thread
            threading.Thread(target=auto_play_youtube, daemon=True).start()
            say(f"Now playing {song_name} by {artist} on YouTube Music, sir.")

        elif platform.lower() == "spotify":
            try:
                # Try Spotify app first
                spotify_uri = f"spotify:search:{encoded_query}"
                result = subprocess.run(['start', spotify_uri], shell=True, capture_output=True)

                if result.returncode == 0:
                    say(f"Playing {song_name} by {artist} on Spotify app, sir.")

                    # Auto-play first result after delay
                    def auto_play_spotify():
                        time.sleep(3)
                        try:
                            # Press Enter to play first result
                            pyautogui.press('enter')
                            time.sleep(1)
                            pyautogui.press('space')  # Start playback
                        except:
                            pass

                    threading.Thread(target=auto_play_spotify, daemon=True).start()
                else:
                    raise Exception("Spotify app not available")

            except:
                # Fallback to Spotify Web Player
                spotify_web_url = f"https://open.spotify.com/search/{encoded_query}"
                webbrowser.open(spotify_web_url)

                def auto_play_spotify_web():
                    time.sleep(5)  # Wait for web player to load
                    try:
                        # Click first song result
                        pyautogui.click(400, 350)
                        time.sleep(1)
                        # Click play button
                        pyautogui.click(500, 400)
                    except:
                        pass

                threading.Thread(target=auto_play_spotify_web, daemon=True).start()
                say(f"Playing {song_name} by {artist} on Spotify web player, sir.")

        return True
    except Exception as e:
        say("Music systems are experiencing difficulties, sir.")
        print(f"Music error: {e}")
        return False

def jarvis_play_youtube_video(search_term):
    """Play YouTube videos with auto-click"""
    try:
        encoded_query = urllib.parse.quote(search_term)
        youtube_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        webbrowser.open(youtube_url)

        def auto_play_video():
            time.sleep(4)  # Wait for page load
            try:
                # Click on first video thumbnail
                click_positions = [
                    (320, 290),  # First video position
                    (300, 270),  # Alternative position
                    (350, 310),  # Another alternative
                ]

                for pos in click_positions:
                    try:
                        pyautogui.click(pos[0], pos[1])
                        break
                    except:
                        continue

            except Exception as e:
                print(f"Auto-play video error: {e}")

        threading.Thread(target=auto_play_video, daemon=True).start()
        say(f"Now playing {search_term} on YouTube, sir.")
        return True

    except Exception as e:
        say("Video playback systems are offline, sir.")
        print(f"YouTube video error: {e}")
        return False

def jarvis_open_spotify_and_play():
    """Open Spotify and start playing music"""
    try:
        # Try to open Spotify app
        try:
            os.system('start spotify:')
            say("Spotify activated, sir. Music systems online.")

            # Auto-play after opening
            def auto_start_music():
                time.sleep(3)
                try:
                    pyautogui.press('space')  # Play/pause toggle
                except:
                    pass

            threading.Thread(target=auto_start_music, daemon=True).start()

        except:
            # Fallback to web player
            webbrowser.open("https://open.spotify.com")
            say("Spotify web player activated, sir.")

        return True
    except Exception as e:
        say("Music systems are offline, sir.")
        return False

def jarvis_send_email_to_address(email_address, subject="", message=""):
    """Send email to specific address like JARVIS"""
    try:
        if not subject:
            subject = "Message from Sohom via SAGE AI"
        if not message:
            message = "This is an automated message sent through SAGE AI assistant."

        # Use AI to enhance the message
        enhanced_message = craft_ai_message(message, "professional")

        success = send_email(email_address, subject, enhanced_message)

        if success:
            say(f"Message transmitted to {email_address}, sir. Communication successful.")
        else:
            say("Message transmission failed, sir. Please check email configuration.")

        return success
    except Exception as e:
        say("Communication systems are offline, sir.")
        print(f"Email error: {e}")
        return False

def craft_ai_message(message, tone="professional"):
    """Use AI to enhance messages"""
    try:
        prompt = f"Enhance this message in a {tone} tone: {message}"

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {apikey}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistralai/devstral-small:free",
            "messages": [
                {
                    "role": "system",
                    "content": f"You are a {tone} message enhancer. Improve the given message while keeping it concise."
                },
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }

        response = requests.post(url, headers=headers, json=data, timeout=15)

        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return message
    except:
        return message

def jarvis_system_status():
    """JARVIS-style system status report"""
    try:
        # Get system information
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        # Network status
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            network_status = "Online"
        except:
            network_status = "Offline"

        # Battery status (if laptop)
        try:
            battery = psutil.sensors_battery()
            if battery:
                battery_status = f"{battery.percent}% {'(Charging)' if battery.power_plugged else '(On Battery)'}"
            else:
                battery_status = "Desktop System"
        except:
            battery_status = "Unknown"

        status_report = f"""
        System Status Report:
        CPU Usage: {cpu_percent}%
        Memory Usage: {memory.percent}%
        Disk Usage: {disk.percent}%
        Network: {network_status}
        Power: {battery_status}
        """

        say(f"System status: CPU at {cpu_percent}%, Memory at {memory.percent}%, Network {network_status}, sir.")
        print(status_report)

        return True
    except Exception as e:
        say("Unable to access system diagnostics, sir.")
        print(f"System status error: {e}")
        return False

def jarvis_weather_report(city=""):
    """JARVIS-style weather report"""
    try:
        if not city:
            # Try to get location automatically
            try:
                g = geocoder.ip('me')
                city = g.city if g.city else "New York"
            except:
                city = "New York"

        # Use OpenWeatherMap API (you'd need to add API key to config)
        # For now, using a placeholder response
        say(f"Weather systems indicate partly cloudy conditions in {city}, sir. Temperature approximately 22 degrees Celsius.")

        return True
    except Exception as e:
        say("Weather monitoring systems are offline, sir.")
        print(f"Weather error: {e}")
        return False

def jarvis_internet_speed():
    """Test internet speed like JARVIS"""
    try:
        say("Initiating network diagnostics, sir.")

        st = speedtest.Speedtest()
        st.get_best_server()

        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000
        ping = st.results.ping

        say(f"Network analysis complete. Download speed: {download_speed:.1f} megabits per second. Upload speed: {upload_speed:.1f} megabits per second. Latency: {ping:.1f} milliseconds, sir.")

        return True
    except Exception as e:
        say("Network diagnostics failed, sir.")
        print(f"Speed test error: {e}")
        return False

def jarvis_search_wikipedia(query):
    """JARVIS-style Wikipedia search"""
    try:
        say(f"Searching knowledge database for {query}, sir.")

        summary = wikipedia.summary(query, sentences=2)
        say(f"According to my knowledge database: {summary}")

        return True
    except Exception as e:
        say(f"Unable to find information about {query} in the knowledge database, sir.")
        return False

def jarvis_stock_price(symbol):
    """Get stock prices like JARVIS"""
    try:
        say(f"Accessing financial markets for {symbol}, sir.")

        stock = yf.Ticker(symbol)
        info = stock.info
        current_price = info.get('currentPrice', 'Unknown')

        say(f"{symbol} is currently trading at {current_price} dollars, sir.")

        return True
    except Exception as e:
        say(f"Unable to access market data for {symbol}, sir.")
        return False

def jarvis_security_protocol():
    """JARVIS-style security features"""
    try:
        say("Initiating security protocols, sir.")

        # Lock the workstation
        os.system("rundll32.exe user32.dll,LockWorkStation")

        return True
    except Exception as e:
        say("Security systems are offline, sir.")
        return False

def jarvis_power_management(action):
    """JARVIS-style power management"""
    try:
        if action == "sleep":
            say("Initiating sleep mode, sir. Systems will be on standby.")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif action == "shutdown":
            say("Initiating shutdown sequence, sir. All systems will be offline.")
            os.system("shutdown /s /t 10")
        elif action == "restart":
            say("Initiating restart sequence, sir. Systems will be back online shortly.")
            os.system("shutdown /r /t 10")

        return True
    except Exception as e:
        say("Power management systems are offline, sir.")
        return False

def open_chrome_tab(url):
    """Open a new tab in Chrome with the specified URL"""
    try:
        # Try to open in Chrome specifically
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        webbrowser.get(chrome_path).open_new_tab(url)
        say(f"Opening {url} in Chrome")
    except:
        # Fallback to default browser
        webbrowser.open_new_tab(url)
        say(f"Opening {url} in browser")

def open_application(app_name):
    """Open Windows applications"""
    apps = {
        "notepad": "notepad",
        "calculator": "calc",
        "paint": "mspaint",
        "word": "winword",
        "excel": "excel",
        "powerpoint": "powerpnt",
        "chrome": "chrome",
        "firefox": "firefox",
        "edge": "msedge",
        "file explorer": "explorer",
        "task manager": "taskmgr",
        "control panel": "control",
        "settings": "ms-settings:",
        "command prompt": "cmd",
        "powershell": "powershell"
    }

    app_name = app_name.lower()
    if app_name in apps:
        try:
            if app_name == "settings":
                os.system(f"start {apps[app_name]}")
            else:
                subprocess.Popen(apps[app_name])
            say(f"Opening {app_name}")
            return True
        except Exception as e:
            say(f"Sorry, I couldn't open {app_name}")
            print(f"App error: {str(e)}")
            return False
    else:
        say(f"Sorry, I don't know how to open {app_name}")
        return False

def say(text, interruptible=True):
    """Simplified and reliable text-to-speech"""
    global is_speaking, should_stop_speaking

    try:
        # Stop any current speech if interrupted
        if should_stop_speaking:
            should_stop_speaking = False
            return

        is_speaking = True

        # Use global TTS engine directly
        if tts_engine:
            try:
                tts_engine.say(text)
                tts_engine.runAndWait()
            except Exception as e:
                # Fallback: create new engine
                try:
                    fallback_tts = pyttsx3.init()
                    fallback_tts.setProperty('rate', 180)
                    fallback_tts.setProperty('volume', 0.9)
                    fallback_tts.say(text)
                    fallback_tts.runAndWait()
                except Exception as e2:
                    print(f"TTS Error: {e2}")
        else:
            print(f"Sage: {text}")  # Fallback to text output

        is_speaking = False

    except Exception as e:
        is_speaking = False
        print(f"TTS Error: {str(e)}")

def stop_speaking():
    """Stop current speech immediately"""
    global should_stop_speaking, is_speaking
    should_stop_speaking = True
    is_speaking = False
    try:
        tts_engine.stop()
    except:
        pass

def takeCommand(continuous=False, timeout=5):
    """Enhanced voice command with Gemini Live-style continuous listening"""
    global is_speaking, should_stop_speaking, conversation_active, last_interaction_time

    r = sr.Recognizer()

    # Enhanced recognizer settings for better performance
    r.energy_threshold = 300
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.8
    r.operation_timeout = None

    with sr.Microphone() as source:
        if not continuous:
            print("🎤 Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)

        print("🎧 Listening..." if not continuous else "🔄 Continuous listening...")

        try:
            # If SAGE is speaking, listen for interruption
            if is_speaking:
                audio = r.listen(source, timeout=1, phrase_time_limit=3)
                try:
                    interruption = r.recognize_google(audio, language="en-in")
                    # Check for interruption keywords
                    interrupt_words = ["stop", "pause", "wait", "sage", "hey", "excuse me"]
                    if any(word in interruption.lower() for word in interrupt_words):
                        stop_speaking()
                        print(f"🛑 Interrupted: {interruption}")
                        return interruption
                except:
                    pass
                return "None"

            # Normal listening
            listen_timeout = timeout if not continuous else 10
            audio = r.listen(source, timeout=listen_timeout, phrase_time_limit=15)

            print("🧠 Processing speech...")

            # Try multiple recognition approaches
            try:
                query = r.recognize_google(audio, language="en-in")
            except:
                try:
                    query = r.recognize_google(audio, language="en-us")
                except:
                    query = r.recognize_google(audio, language="en-gb")

            print(f"👤 User said: {query}")

            # Update conversation state
            conversation_active = True
            last_interaction_time = datetime.datetime.now()

            return query.lower().strip()

        except sr.WaitTimeoutError:
            if continuous:
                return "timeout_continue"
            print("⏰ Listening timeout")
            return "None"
        except sr.UnknownValueError:
            if continuous:
                return "unknown_continue"
            print("❓ Could not understand audio")
            return "None"
        except sr.RequestError as e:
            print(f"🚫 Speech service error: {e}")
            return "None"
        except Exception as e:
            print(f"❌ Error occurred: {str(e)}")
            return "Some Error Occurred. Sorry from Sage"

def continuous_conversation_mode():
    """Gemini Live-style continuous conversation"""
    global conversation_active, continuous_listening

    say("Entering continuous conversation mode. I'll keep listening until you say 'exit conversation' or stay quiet for 30 seconds.")
    continuous_listening = True
    conversation_active = True

    while continuous_listening and conversation_active:
        query = takeCommand(continuous=True, timeout=30)

        if query in ["timeout_continue", "unknown_continue"]:
            # Check if conversation should timeout
            if last_interaction_time and (datetime.datetime.now() - last_interaction_time).seconds > 30:
                say("Conversation timeout. Returning to normal mode.")
                break
            continue

        if query == "None":
            continue

        # Exit conditions
        if any(phrase in query for phrase in ["exit conversation", "stop conversation", "end conversation"]):
            say("Exiting continuous conversation mode.")
            break

        # Process the command normally
        process_voice_command(query)

    continuous_listening = False
    conversation_active = False

def process_voice_command(query):
    """Process voice commands with context awareness like Gemini Live"""
    global chatStr, conversation_active

    # Handle interruption commands first
    if any(word in query for word in ["stop", "pause", "quiet", "silence"]):
        stop_speaking()
        say("Understood, sir.")
        return

    # Context-aware responses
    if conversation_active:
        # Add conversational context
        context_phrases = [
            "Also, ", "Additionally, ", "Furthermore, ", "By the way, ",
            "Speaking of which, ", "That reminds me, "
        ]

        # Natural conversation starters
        if any(phrase in query for phrase in ["what about", "how about", "tell me about"]):
            # More conversational response
            pass

    # Process commands with the main command logic
    # This will call the main command processing logic

def enhance_response_with_context(response, query):
    """Enhance responses with conversational context like Gemini Live"""
    global conversation_active, last_interaction_time

    if not conversation_active:
        return response

    # Add conversational elements
    conversation_starters = [
        "Certainly, sir. ",
        "Of course, Mr. Sohom. ",
        "Right away, sir. ",
        "Absolutely, sir. "
    ]

    # Add follow-up suggestions
    follow_ups = {
        "music": "Would you like me to adjust the volume or skip to another track?",
        "email": "Should I send any other messages while we're at it?",
        "weather": "Would you like me to check the forecast for tomorrow as well?",
        "system": "Shall I run any system optimizations while I'm at it?",
        "search": "Would you like me to search for anything else related to this topic?"
    }

    # Detect command type and add appropriate follow-up
    for cmd_type, follow_up in follow_ups.items():
        if cmd_type in query:
            if random.random() < 0.3:  # 30% chance to add follow-up
                response += f" {follow_up}"
            break

    return response

def natural_language_processing(query):
    """Process natural language like Gemini Live"""
    # Handle conversational queries
    conversational_patterns = {
        "how are you": "I'm functioning optimally, sir. All systems are running smoothly.",
        "what can you do": "I can control music, send emails, manage your system, search for information, and much more. What would you like me to help you with?",
        "thank you": "You're very welcome, Mr. Sohom. Always happy to assist.",
        "good job": "Thank you, sir. I'm here to serve.",
        "that's wrong": "I apologize for the error, sir. Let me correct that for you.",
        "try again": "Of course, sir. Let me attempt that once more.",
        "never mind": "Understood, sir. Is there anything else I can help you with?",
        "what time": f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}, sir.",
        "what day": f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}, sir.",
        "good morning": f"Good morning, Mr. Sohom! Ready to assist you today.",
        "good afternoon": f"Good afternoon, sir! How may I help you?",
        "good evening": f"Good evening, Mr. Sohom! At your service.",
        "hello": "Hello, sir! How may I assist you today?",
        "hi": "Hello, Mr. Sohom! What can I do for you?"
    }

    for pattern, response in conversational_patterns.items():
        if pattern in query.lower():
            return response

    return None

def smart_wake_word_detection(query):
    """Detect wake words and context like Gemini Live"""
    wake_words = ["sage", "hey sage", "okay sage", "jarvis", "computer"]

    for wake_word in wake_words:
        if wake_word in query.lower():
            # Remove wake word and return clean command
            clean_query = query.lower().replace(wake_word, "").strip()
            if clean_query:
                return clean_query
            else:
                return "listening"

    return query

# Legacy main execution removed - using new enhanced main() function
# All legacy command processing removed - using new enhanced system


def main():
    """Main function to run the enhanced voice assistant"""
    global sage_instance
    try:
        # Initialize the advanced AI assistant
        sage = AdvancedSageAI()
        sage_instance = sage  # Set global reference

        # Always ask which AI model to use for this session
        sage.ask_ai_preference()

        # Welcome message
        welcome_messages = [
            f"Hello {sage.user_name}! Sage AI is now online and ready to assist you.",
            f"Good to see you, {sage.user_name}! How can I help you today?",
            f"Sage AI systems are fully operational, {sage.user_name}. What can I do for you?",
            f"Welcome back, {sage.user_name}! I'm here and ready to help."
        ]

        welcome = random.choice(welcome_messages)
        sage.say(welcome)

        # Show current AI model
        current_model = sage.ai_models.get(sage.preferred_ai, "Unknown")
        console.print(f"[cyan]Current AI Model: {current_model}[/cyan]")

        console.print("\n[bold yellow]🎤 Voice Commands:[/bold yellow]")
        console.print("• Say 'Sage' or 'Hey Sage' to activate")
        console.print("• Say 'continuous mode on' for hands-free operation")
        console.print("• Say 'change AI model' to switch between Gemini and LLM")
        console.print("• Say 'which AI' to check current AI model")
        console.print("• Say 'camera' or 'open camera' to open camera app")
        console.print("• Say 'Google', 'YouTube', 'Spotify' to open directly (no 'open' needed)")
        console.print("• Say 'open calculator', 'open notepad', etc. for apps")
        console.print("• Say 'play music', 'send email', 'what time is it'")
        console.print("• Say 'goodbye', 'bye', or 'exit' to quit")
        console.print("• Ask any questions for AI responses\n")

        # Main listening loop
        while True:
            try:
                if sage.continuous_mode:
                    # In continuous mode, always listen for commands
                    command = sage.listen_for_command(timeout=30)
                    if command and command not in ["timeout", "unknown", "error"]:
                        if not sage.process_voice_command(command):
                            break
                else:
                    # Wait for wake word
                    wake_command = sage.listen_for_command(timeout=30, wake_word_mode=True)

                    if wake_command and wake_command != "timeout":
                        # Check if wake word is detected
                        if any(wake_word in wake_command for wake_word in sage.wake_words):
                            console.print(f"[green]✓ Wake word detected![/green]")
                            sage.say("Yes?")

                            # Listen for actual command
                            command = sage.listen_for_command(timeout=15)
                            if command and command not in ["timeout", "unknown", "error"]:
                                if not sage.process_voice_command(command):
                                    break
                        elif any(exit_word in wake_command for exit_word in sage.exit_words):
                            # Direct exit command
                            sage.say(f"Goodbye {sage.user_name}! Have a great day!")
                            break

                # Small delay to prevent excessive CPU usage
                time.sleep(0.1)

            except KeyboardInterrupt:
                console.print("\n[yellow]Keyboard interrupt detected[/yellow]")
                sage.say("Goodbye! Shutting down.")
                break
            except Exception as e:
                logger.error(f"Main loop error: {e}")
                console.print(f"[red]Error in main loop: {e}[/red]")
                time.sleep(1)

    except Exception as e:
        console.print(f"[red]Failed to initialize Sage AI: {e}[/red]")
        logger.error(f"Initialization error: {e}")

    finally:
        console.print("\n[bold red]🤖 Sage AI Shutting Down[/bold red]")
        console.print("[green]Thank you for using Sage AI![/green]")


if __name__ == "__main__":
    main()

