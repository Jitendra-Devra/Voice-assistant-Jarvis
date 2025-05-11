#!/usr/bin/env python3
# main.py - Core file that runs the voice assistant loop

import time
import speech_recognition as sr
from voice_input import listen_for_command
from voice_output import speak
from commands import (
    handle_greeting,
    handle_goodbye,
    handle_time,
    handle_weather,
    handle_search,
    handle_open_app,
    handle_unknown,
    handle_youtube,
    handle_whatsapp
)

def process_command(command):
    """Process the recognized command and route to appropriate handler"""
    command = command.lower()
    
    # Simple command routing based on keywords
    if not command:
        return
        
    print(f"Command recognized: {command}")
    
    # Check for Jarvis name in command (optional activation)
    if "jarvis" in command:
        command = command.replace("jarvis", "").strip()
    
    # Greeting commands
    if any(word in command for word in ["hello", "hi", "hey", "greetings"]):
        return handle_greeting()
        
    # Time commands
    elif any(word in command for word in ["time", "what time", "clock"]):
        return handle_time()
        
    # Weather commands
    elif any(word in command for word in ["weather", "temperature", "forecast"]):
        return handle_weather(command)
        
    # WhatsApp commands - check before general search to avoid conflicts
    elif "whatsapp" in command:
        return handle_whatsapp(command)
        
    # YouTube commands - check before general search to avoid conflicts
    elif any(word in command for word in ["youtube", "play", "watch", "video"]):
        return handle_youtube(command)
        
    # Search commands
    elif any(word in command for word in ["search", "google", "look up", "find"]):
        return handle_search(command)
        
    # Open application commands
    elif any(word in command for word in ["open", "launch", "start", "run"]):
        return handle_open_app(command)
        
    # Exit commands
    elif any(word in command for word in ["exit", "quit", "goodbye", "bye", "stop", "end"]):
        return handle_goodbye()
        
    # Default response
    else:
        return handle_unknown()

def main():
    """Main function that runs the voice assistant loop"""
    speak("Jarvis is now active. How can I help you?")
    
    while True:
        try:
            command = listen_for_command()
            response = process_command(command)
            
            if response == "exit":
                break
                
        except Exception as e:
            print(f"Error: {e}")
            speak("Sorry, something went wrong. Please try again.")
            
if __name__ == "__main__":
    main()