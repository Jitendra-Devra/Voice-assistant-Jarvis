#!/usr/bin/env python3
# commands.py - Enhanced command handling with better recognition and debugging

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
from os_operations import open_recycle_bin, empty_recycle_bin

def preprocess_command(command):
    """
    Preprocess the command for better recognition
    """
    if not command:
        return ""
    
    # Convert to lowercase and strip whitespace
    command = command.lower().strip()
    
    # Remove punctuation that might interfere but preserve important ones
    command = re.sub(r'[^\w\s\-\'\"]+', ' ', command)
    
    # Replace common variations and improve recognition
    replacements = {
        'recycling bin': 'recycle bin',
        'trash can': 'recycle bin',
        'trash bin': 'recycle bin',
        'waste bin': 'recycle bin',
        'garbage': 'recycle bin',
        'garbage bin': 'recycle bin',
        'recycle': 'recycle bin',
        'open recycling': 'open recycle bin',
        'open trash': 'open recycle bin',
        'empty recycling': 'empty recycle bin',
        'empty trash': 'empty recycle bin',
        'clear recycle bin': 'empty recycle bin',
        'delete recycle bin': 'empty recycle bin',
        
        # Time variations
        'what is the time': 'time',
        'tell me the time': 'time',
        'current time': 'time',
        'what time is it': 'time',
        
        # Search variations
        'google search': 'search',
        'search google': 'search',
        'look for': 'search',
        'find on internet': 'search',
        'search for': 'search',
        
        # YouTube variations
        'youtube video': 'youtube',
        'play video': 'youtube',
        'watch video': 'youtube',
        'open youtube': 'youtube',
        
        # App opening variations
        'launch application': 'open',
        'start program': 'open',
        'run application': 'open',
        'start app': 'open',
        'launch': 'open',
        'start': 'open',
        'run': 'open',
        
        # Common misrecognitions
        'reciting': 'recycle',
        'recycling': 'recycle',
        'recipe': 'recycle',
        'recent': 'recycle',
        'receive': 'recycle',
    }
    
    # Apply replacements
    for old, new in replacements.items():
        command = command.replace(old, new)
    
    # Remove extra whitespace
    command = ' '.join(command.split())
    
    return command

def debug_command(original_command, processed_command, matched_category=None):
    """
    Debug function to help understand command processing
    """
    print(f"DEBUG - Original: '{original_command}'")
    print(f"DEBUG - Processed: '{processed_command}'")
    if matched_category:
        print(f"DEBUG - Matched category: {matched_category}")
    print("-" * 50)

def handle_os_command(command, gui):
    """Handles OS-level commands like interacting with the Recycle Bin."""
    debug_command(command, command, "OS Command")
    
    # More comprehensive matching for recycle bin commands
    recycle_keywords = ['recycle', 'bin', 'trash', 'garbage', 'waste']
    open_keywords = ['open', 'show', 'display', 'access', 'view']
    empty_keywords = ['empty', 'clear', 'delete', 'clean', 'remove']
    
    command_lower = command.lower()
    command_words = command_lower.split()
    
    # Check for recycle bin mentions
    has_recycle = any(keyword in command_lower for keyword in recycle_keywords)
    has_open = any(keyword in command_lower for keyword in open_keywords)
    has_empty = any(keyword in command_lower for keyword in empty_keywords)
    
    print(f"DEBUG - Recycle command analysis:")
    print(f"  Command: '{command}'")
    print(f"  Has recycle: {has_recycle}")
    print(f"  Has open: {has_open}")
    print(f"  Has empty: {has_empty}")
    
    if has_recycle:
        if has_empty:
            speak("Warning: this action is permanent and cannot be undone.", gui)
            empty_recycle_bin(gui)
        elif has_open or not has_empty:  # Default to open if not explicitly empty
            speak("Opening the recycle bin now.", gui)
            open_recycle_bin(gui)
    else:
        speak("I'm not sure which OS action you mean. Try saying 'open recycle bin' or 'empty recycle bin'.", gui)

def handle_greeting(gui):
    """Handle greeting commands"""
    greetings = [
        "Hello! This is Jarvis. How can I help you today?",
        "Hi there! Jarvis at your service. What can I do for you?",
        "Hey! Jarvis here. What do you need?",
        "Greetings! Jarvis ready to assist you."
    ]
    response = random.choice(greetings)
    speak(response, gui)

def handle_goodbye(gui):
    """Handle exit commands"""
    speak("Shutting down, sir. Jarvis going offline.", gui)
    return "exit"

def handle_time(gui):
    """Handle time requests"""
    current_time = datetime.datetime.now().strftime('%I:%M %p')
    current_date = datetime.datetime.now().strftime('%A, %B %d, %Y')
    response = f"The current time is {current_time} on {current_date}"
    speak(response, gui)

def handle_weather(command, gui):
    """
    Handle weather requests with improved city detection
    """
    debug_command(command, command, "Weather")
    
    words = command.split()
    city = None
    
    # Look for city patterns
    patterns = [
        r'weather (?:in|for|at|of) ([a-zA-Z\s]+)',
        r'(?:in|for|at|of) ([a-zA-Z\s]+) weather',
        r'weather ([a-zA-Z\s]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, command, re.IGNORECASE)
        if match:
            city = match.group(1).strip()
            # Remove common words that might be picked up
            city_words = [word for word in city.split() if word.lower() not in ['the', 'is', 'like', 'what']]
            city = ' '.join(city_words)
            break
    
    if not city or len(city) < 2:
        # Default city for India (since you're in Gujarat)
        city = "Ahmedabad"
        speak(f"No city specified. Showing weather for {city}.", gui)

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if response.status_code == 200:
            temperature = data['main']['temp']
            condition = data['weather'][0]['description']
            humidity = data['main']['humidity']
            feels_like = data['main']['feels_like']
            
            weather_info = f"The weather in {city} is {condition} with a temperature of {temperature:.1f}°C, feels like {feels_like:.1f}°C, and humidity at {humidity}%"
            speak(weather_info, gui)
        else:
            speak(f"Sorry, I couldn't find weather information for {city}.", gui)
            
    except requests.RequestException as e:
        speak("Sorry, there was an error connecting to the weather service.", gui)
        print(f"Weather API error: {e}")
    except Exception as e:
        speak("Sorry, there was an error getting the weather.", gui)
        print(f"Weather error: {e}")

def handle_search(command, gui):
    """
    Handle web search requests with improved search capability
    """
    debug_command(command, command, "Search")
    
    # Multiple patterns to extract search query
    patterns = [
        r'(?:search|google|look up|find)(?: for)?\s+(.+)',
        r'(?:search|google|look up|find)\s+(.+)',
        r'(.+?)\s+(?:on google|search)',
    ]
    
    query = None
    for pattern in patterns:
        match = re.search(pattern, command, re.IGNORECASE)
        if match:
            query = match.group(1).strip()
            break
    
    # Fallback: remove search keywords from command
    if not query:
        search_words = ['search', 'google', 'look up', 'find', 'for']
        words = command.split()
        filtered_words = [word for word in words if word not in search_words]
        query = ' '.join(filtered_words)
    
    if query and len(query.strip()) > 0:
        speak(f"Searching for {query}", gui)
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(search_url)
    else:
        speak("What would you like me to search for?", gui)

def handle_youtube(command, gui):
    """
    Enhanced YouTube handler with better pattern matching
    """
    debug_command(command, command, "YouTube")
    
    # Pattern to extract what to search for
    patterns = [
        r'(?:youtube|play|watch)\s+(.+)',
        r'(.+?)\s+(?:on youtube|youtube)',
        r'(?:open youtube and (?:search|find|play|watch))\s+(.+)',
    ]
    
    query = None
    for pattern in patterns:
        match = re.search(pattern, command, re.IGNORECASE)
        if match:
            query = match.group(1).strip()
            # Remove common stop words
            stop_words = ['video', 'videos', 'on', 'youtube']
            query_words = [word for word in query.split() if word.lower() not in stop_words]
            query = ' '.join(query_words)
            break
    
    if query and len(query.strip()) > 0:
        speak(f"Searching YouTube for {query}", gui)
        youtube_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(youtube_url)
    else:
        speak("Opening YouTube.", gui)
        webbrowser.open("https://www.youtube.com")

def handle_whatsapp(command, gui):
    """
    Enhanced WhatsApp handler
    """
    debug_command(command, command, "WhatsApp")
    
    # Pattern for sending message
    message_pattern = r'(?:whatsapp|message|text)\s+(.+?)\s+(?:saying|that)\s+(.+)'
    match = re.search(message_pattern, command, re.IGNORECASE)
    
    if match:
        contact = match.group(1).strip()
        message = match.group(2).strip()
        
        if os.name == 'nt':
            try:
                speak(f"Opening WhatsApp to message {contact}.", gui)
                encoded_message = message.replace(' ', '%20')
                subprocess.Popen(f"start whatsapp://send?text={encoded_message}", shell=True)
                return
            except Exception as e:
                print(f"Error launching WhatsApp app: {e}")
    
    # Just open WhatsApp
    speak("Opening WhatsApp.", gui)
    if os.name == 'nt':
        try:
            subprocess.Popen("start whatsapp:", shell=True)
        except:
            webbrowser.open("https://web.whatsapp.com/")
    else:
        webbrowser.open("https://web.whatsapp.com/")

def handle_open_app(command, gui):
    """
    Handle requests to open applications with improved app name detection
    """
    debug_command(command, command, "Open App")
    
    # Remove "open", "launch", "start", "run" from the command
    app_name = command
    for keyword in ['open', 'launch', 'start', 'run']:
        app_name = re.sub(rf'\b{keyword}\b', '', app_name, flags=re.IGNORECASE)
    
    app_name = app_name.strip()
    
    if not app_name:
        speak("Which application would you like to open?", gui)
        return
    
    # Handle special cases and common names
    app_mappings = {
        'visual studio code': 'code',
        'vs code': 'code',
        'vscode': 'code',
        'google chrome': 'chrome',
        'chrome browser': 'chrome',
        'web browser': 'chrome',
        'browser': 'chrome',
        'text editor': 'notepad',
        'calculator': 'calculator',
        'calc': 'calculator',
        'command prompt': 'cmd',
        'terminal': 'cmd',
        'file explorer': 'explorer',
        'explorer': 'explorer'
    }
    
    # Check for direct mapping
    if app_name.lower() in app_mappings:
        app_name = app_mappings[app_name.lower()]
    
    # Clean app name
    app_name = re.sub(r'[^\w\s]', '', app_name).strip().lower()
    
    print(f"DEBUG - Looking for app: '{app_name}'")
    print(f"DEBUG - Available apps: {list(APP_PATHS.keys())}")
    
    if app_name in APP_PATHS:
        path = APP_PATHS[app_name]
        try:
            speak(f"Opening {app_name}", gui)
            if os.name == 'nt':
                if path.endswith('.exe') or '\\' in path:
                    os.startfile(path)
                else:
                    # Protocol handler (like whatsapp:)
                    subprocess.run(f'start {path}', shell=True)
            else:
                subprocess.Popen(shlex.split(path))
        except Exception as e:
            speak(f"Sorry, I couldn't open {app_name}", gui)
            print(f"Error opening app: {e}")
    else:
        # Try to find a partial match
        matches = [app for app in APP_PATHS.keys() if app_name in app or app in app_name]
        if matches:
            best_match = matches[0]
            try:
                speak(f"Opening {best_match}", gui)
                path = APP_PATHS[best_match]
                if os.name == 'nt':
                    if path.endswith('.exe') or '\\' in path:
                        os.startfile(path)
                    else:
                        subprocess.run(f'start {path}', shell=True)
                else:
                    subprocess.Popen(shlex.split(path))
            except Exception as e:
                speak(f"Sorry, I couldn't open {best_match}", gui)
                print(f"Error opening app: {e}")
        else:
            available_apps = ', '.join(list(APP_PATHS.keys())[:5])  # Show first 5
            speak(f"Sorry, I don't know how to open {app_name}. Some available apps are: {available_apps}", gui)

def handle_unknown(gui):
    """Handle commands that don't match any known patterns"""
    responses = [
        "I'm not sure I understand, sir. Could you rephrase that?",
        "I didn't catch that. What would you like me to do?",
        "Sorry, I don't know how to help with that yet. Try commands like 'what time is it', 'open recycle bin', or 'search for something'.",
        "I'm still learning. Could you try a different command? Say 'help' to see what I can do."
    ]
    response = random.choice(responses)
    speak(response, gui)

def handle_help(gui):
    """Provide help information about available commands"""
    help_text = """Here are some commands you can try:
    - What time is it?
    - What's the weather in London?
    - Open recycle bin
    - Empty recycle bin
    - Search for Python tutorials
    - Open Chrome
    - Play music on YouTube
    - Open WhatsApp
    - Open notepad
    - Goodbye to exit"""
    
    speak(help_text, gui)