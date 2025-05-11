#!/usr/bin/env python3
# commands.py - Handles different command actions (weather, search, apps, etc.)

import webbrowser
import datetime
import random
import os
import subprocess
import requests
import re
import time
import shlex
from voice_output import speak
from config import OPENWEATHER_API_KEY, APP_PATHS

def handle_greeting():
    """Handle greeting commands"""
    greetings = [
        "Hello! This is Jarvis. How can I help you today?",
        "Hi there! Jarvis at your service. What can I do for you?",
        "Hey! Jarvis here. What do you need?",
        "Greetings! Jarvis ready to assist you."
    ]
    response = random.choice(greetings)
    speak(response)

def handle_goodbye():
    """Handle exit commands"""
    speak("Shutting down, sir. Jarvis going offline.")
    return "exit"

def handle_time():
    """Handle time requests"""
    current_time = datetime.datetime.now().strftime('%I:%M %p')
    response = f"The current time is {current_time}"
    speak(response)

def handle_weather(command):
    """
    Handle weather requests
    
    Args:
        command (str): User's voice command
    """
    # Extract city name from command
    # This is a simple extraction - could be improved with NLP
    words = command.split()
    city = None
    
    # Try to find city after keywords like "in" or "for"
    for i, word in enumerate(words):
        if word in ["in", "for", "at"] and i < len(words) - 1:
            city = words[i + 1]
            # Check if next word is also part of city name (e.g., "New York")
            if i + 2 < len(words) and words[i + 2] not in ["weather", "temperature", "like"]:
                city += " " + words[i + 2]
            break
    
    # If no city found in command, ask the user
    if not city:
        speak("Which city would you like the weather for?")
        # In a real app, you'd listen for the city here
        city = "London"  # Default city
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            temperature = data['main']['temp']
            condition = data['weather'][0]['description']
            humidity = data['main']['humidity']
            feels_like = data['main']['feels_like']
            
            weather_info = f"The weather in {city} is {condition} with a temperature of {temperature:.1f}°C, feels like {feels_like:.1f}°C, and humidity at {humidity}%"
            speak(weather_info)
        else:
            speak(f"Sorry, I couldn't find weather information for {city}")
            
    except Exception as e:
        speak(f"Sorry, there was an error getting the weather. Please check your API key and try again.")
        print(f"Weather API error: {e}")

def handle_search(command):
    """
    Handle web search requests with improved search capability

    Args:
        command (str): User's voice command
    """
    # Improved pattern: match "search", "google", "look up", "find" at start or anywhere
    pattern = r"(?:search|google|look up|find)(?: for)?\s*(.+)"
    match = re.search(pattern, command, re.IGNORECASE)
    query = None

    if match:
        query = match.group(1).strip()
    else:
        # Fallback: if command starts with just the keyword
        for keyword in ["search", "google", "look up", "find"]:
            if command.lower().startswith(keyword):
                query = command[len(keyword):].strip()
                break

    if query:
        speak(f"Searching for {query}")
        chrome_path = APP_PATHS.get("chrome", None)
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        if chrome_path and os.path.exists(chrome_path):
            if os.name == 'nt':
                webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
                webbrowser.get('chrome').open(search_url)
            else:
                subprocess.Popen([chrome_path, search_url])
        else:
            webbrowser.open(search_url)
    else:
        speak("What would you like me to search for?")

def handle_youtube(command):
    """
    Enhanced YouTube handler that can play videos from specific creators
    
    Args:
        command (str): User's voice command
    """
    # Pattern for "play [creator]'s video" or "watch [creator]'s video"
    creator_pattern = r"(?:open )?youtube(?: and)? (?:play|watch) (.+?)(?:'s)?(?: video| channel)?"
    match = re.search(creator_pattern, command, re.IGNORECASE)
    
    if match:
        creator = match.group(1).strip()
        speak(f"Playing videos from {creator} on YouTube")
        youtube_url = f"https://www.youtube.com/results?search_query={creator.replace(' ', '+')}"
        
        # Open YouTube search results
        webbrowser.open(youtube_url)
        
        # Wait for page to load and then simulate clicking on the first video
        # Note: This is an approximation and may not work in all environments
        # For a more reliable solution, consider using Selenium WebDriver
        time.sleep(3)  # Wait for page to load
        try:
            if os.name == 'nt':  # Windows
                # Simulate TAB and ENTER keys to navigate to first video (may vary by browser)
                os.system("PowerShell -Command \"$wshell = New-Object -ComObject wscript.shell; $wshell.SendKeys('{TAB}'); Start-Sleep -m 500; $wshell.SendKeys('{TAB}'); Start-Sleep -m 500; $wshell.SendKeys('{ENTER}')\"")
            else:  # Linux-based systems with xdotool
                subprocess.run(["xdotool", "key", "Tab", "Tab", "Return"])
        except Exception as e:
            print(f"Error automating video click: {e}")
        return

    # Regular YouTube search pattern
    pattern = r"(?:open )?youtube(?: and)? (?:search|find|look up|play|watch)? ?(.+)?"
    match = re.search(pattern, command, re.IGNORECASE)
    if match and match.group(1):
        query = match.group(1).strip()
        speak(f"Searching YouTube for {query}")
        youtube_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(youtube_url)
        return

    # Fallback: just open YouTube
    speak("Opening YouTube")
    webbrowser.open("https://www.youtube.com")

def handle_whatsapp(command):
    """
    Enhanced WhatsApp handler that can open desktop app and message contacts
    
    Args:
        command (str): User's voice command
    """
    # Windows Store app pattern
    ms_store_pattern = r"(?:open )?whatsapp(?: and)? (?:message|msg|text|send) ([\w\s]+?) (?:saying |that )?(.*)"
    match = re.search(ms_store_pattern, command, re.IGNORECASE)
    
    if match:
        contact = match.group(1).strip()
        message = match.group(2).strip()
        
        # For Windows Store WhatsApp Desktop app
        if os.name == 'nt':
            try:
                # First try to open WhatsApp desktop app using Windows URI protocol
                speak(f"Opening WhatsApp and preparing message for {contact}")
                
                # Try to use WhatsApp protocol URI (works with WhatsApp Desktop app)
                encoded_message = message.replace(' ', '%20')
                subprocess.Popen(f"start whatsapp://send?text={encoded_message}", shell=True)
                
                speak(f"Please select {contact} from your contacts to send: {message}")
                return
            except Exception as e:
                print(f"Error launching WhatsApp app: {e}")
                # Fall back to web version below
        
    # Web WhatsApp pattern (fallback)
    web_pattern = r"(?:open )?whatsapp(?: web)?(?: and)? (?:message|msg|text) ([\w\s]+?) (.+)"
    match = re.search(web_pattern, command, re.IGNORECASE)
    if match:
        contact = match.group(1).strip()
        message = match.group(2).strip()
        # WhatsApp Web API for prefilled message (user must select contact manually)
        url = f"https://web.whatsapp.com/send?text={message.replace(' ', '%20')}"
        speak(f"Opening WhatsApp Web. Please select {contact} and send your message.")
        webbrowser.open(url)
        return

    # Fallback: just open WhatsApp
    if "whatsapp" in command:
        try:
            # Try to open the Windows Store app if on Windows
            if os.name == 'nt':
                try:
                    # Try using the Microsoft Store app protocol
                    subprocess.Popen("start whatsapp:", shell=True)
                    speak("Opening WhatsApp desktop app")
                except:
                    # Fallback to web version
                    webbrowser.open("https://web.whatsapp.com/")
                    speak("Opening WhatsApp Web")
            else:
                # Non-Windows platforms default to web
                webbrowser.open("https://web.whatsapp.com/")
                speak("Opening WhatsApp Web")
        except Exception as e:
            print(f"Error opening WhatsApp: {e}")
            speak("Sorry, I couldn't open WhatsApp")

def handle_open_app(command):
    """
    Handle requests to open applications

    Args:
        command (str): User's voice command
    """
    app_name = None
    words = command.split()

    # Improved: support "open vscode", "open visual studio code", etc.
    for i, word in enumerate(words):
        if word == "open" and i < len(words) - 1:
            # Try to match multi-word app names
            next_words = " ".join(words[i+1:i+4]).lower()
            if "visual studio code" in next_words:
                app_name = "code"
                break
            elif "vscode" in next_words:
                app_name = "code"
                break
            else:
                app_name = words[i + 1].lower()
                # Check if next word is also part of app name (e.g., "visual studio")
                if i + 2 < len(words):
                    app_name += " " + words[i + 2].lower()
                break

    if not app_name:
        speak("Which application would you like to open?")
        return

    app_name = re.sub(r'[^\w\s]', '', app_name).strip()

    # Add support for "vscode" and "visual studio code"
    if app_name in ["vscode", "visual studio code"]:
        app_name = "code"

    if app_name in APP_PATHS:
        path = APP_PATHS[app_name]
        try:
            if os.name == 'nt':
                os.startfile(path)
            else:
                subprocess.Popen(shlex.split(path))
            speak(f"Opening {app_name}")
        except Exception as e:
            speak(f"Sorry, I couldn't open {app_name}")
            print(f"Error opening app: {e}")
    else:
        common_apps = {
            "chrome": "google-chrome" if os.name != 'nt' else "chrome",
            "firefox": "firefox",
            "notepad": "notepad" if os.name == 'nt' else "gedit",
            "calculator": "calc" if os.name == 'nt' else "gnome-calculator",
            "whatsapp": "whatsapp:" if os.name == 'nt' else None,
            "code": APP_PATHS.get("code", None),  # VS Code
        }
        found = False
        for common_name, exec_name in common_apps.items():
            if common_name in app_name and exec_name:
                try:
                    if os.name == 'nt':
                        if common_name == "whatsapp":
                            subprocess.Popen(f"start {exec_name}", shell=True)
                        else:
                            os.system(f"start {exec_name}")
                    else:
                        subprocess.Popen(shlex.split(exec_name))
                    speak(f"Opening {common_name}")
                    found = True
                    break
                except Exception:
                    pass
        if not found:
            speak(f"Sorry, I don't know how to open {app_name}")

def handle_unknown():
    """Handle commands that don't match any known patterns"""
    responses = [
        "I'm not sure I understand, sir. Could you rephrase that?",
        "I didn't catch that. What would you like me to do?",
        "Sorry, I don't know how to help with that yet.",
        "I'm still learning. Could you try a different command?"
    ]
    response = random.choice(responses)
    speak(response)