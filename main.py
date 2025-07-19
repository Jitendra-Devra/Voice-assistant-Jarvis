#!/usr/bin/env python3
# main.py - Enhanced voice assistant with better command processing

import time
import speech_recognition as sr
import threading
import customtkinter as ctk
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
    handle_whatsapp,
    handle_os_command,
    handle_help,
    preprocess_command,
    debug_command
)

from gui import JarvisGUI

# GUI object will be shared
gui = None

def process_command(command):
    """Process the recognized command with improved routing"""
    if not command:
        return
    
    original_command = command
    command = preprocess_command(command)
    
    gui.update_transcription(original_command)
    
    # Debug output
    debug_command(original_command, command)
    
    # Check for Jarvis name in command (optional activation)
    if "jarvis" in command:
        command = command.replace("jarvis", "").strip()
    
    # Skip empty commands
    if not command:
        return
    
    # --- Enhanced Command Routing with Priority ---
    # Most specific commands first, then general ones
    
    # Exit commands - highest priority
    exit_keywords = ["exit", "quit", "goodbye", "bye", "stop", "end", "shutdown"]
    if any(keyword in command for keyword in exit_keywords):
        debug_command(original_command, command, "EXIT")
        return handle_goodbye(gui)
    
    # Help command
    if "help" in command:
        debug_command(original_command, command, "HELP")
        return handle_help(gui)
    
    # Greeting commands
    greeting_keywords = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"]
    if any(keyword in command for keyword in greeting_keywords):
        debug_command(original_command, command, "GREETING")
        return handle_greeting(gui)
    
    # Time commands
    time_keywords = ["time", "clock", "what time"]
    if any(keyword in command for keyword in time_keywords):
        debug_command(original_command, command, "TIME")
        return handle_time(gui)
    
    # Weather commands
    weather_keywords = ["weather", "temperature", "forecast", "climate"]
    if any(keyword in command for keyword in weather_keywords):
        debug_command(original_command, command, "WEATHER")
        return handle_weather(command, gui)
    
    # OS commands - Recycle bin operations (high priority for specificity)
    recycle_keywords = ["recycle bin", "trash", "garbage", "waste bin"]
    if any(keyword in command for keyword in recycle_keywords):
        debug_command(original_command, command, "OS_COMMAND")
        return handle_os_command(command, gui)
    
    # WhatsApp commands
    if "whatsapp" in command:
        debug_command(original_command, command, "WHATSAPP")
        return handle_whatsapp(command, gui)
    
    # YouTube commands - check for YouTube specifically
    youtube_keywords = ["youtube", "play video", "watch video"]
    youtube_in_command = any(keyword in command for keyword in youtube_keywords)
    general_play_keywords = ["play", "watch"] # These could be YouTube or other media
    
    if youtube_in_command or (any(keyword in command for keyword in general_play_keywords) and "youtube" not in command):
        # If it's clearly YouTube or a general play command, handle it as YouTube
        debug_command(original_command, command, "YOUTUBE")
        return handle_youtube(command, gui)
    
    # Search commands
    search_keywords = ["search", "google", "look up", "find", "search for"]
    if any(keyword in command for keyword in search_keywords):
        debug_command(original_command, command, "SEARCH")
        return handle_search(command, gui)
    
    # Open application commands
    open_keywords = ["open", "launch", "start", "run"]
    if any(keyword in command for keyword in open_keywords):
        debug_command(original_command, command, "OPEN_APP")
        return handle_open_app(command, gui)
    
    # If no specific command matched, try to infer intent
    # Check if it might be a search query
    if len(command.split()) > 2 and not any(char in command for char in "?!"):
        debug_command(original_command, command, "INFERRED_SEARCH")
        speak("I'll search for that on Google.", gui)
        return handle_search("search " + command, gui)
    
    # Default to unknown command
    debug_command(original_command, command, "UNKNOWN")
    return handle_unknown(gui)

def assistant_thread_func():
    """Main function that runs the voice assistant loop"""
    global gui
    speak("Jarvis is now active. How can I help you? Say 'help' to see available commands.", gui)
    
    consecutive_errors = 0
    max_consecutive_errors = 5
    
    while True:
        try:
            command = listen_for_command(gui)
            
            # Reset error counter on successful command
            if command:
                consecutive_errors = 0
            
            response = process_command(command)
            
            if response == "exit":
                gui.root.quit() # Properly close the GUI
                break
                
        except KeyboardInterrupt:
            speak("Shutting down Jarvis.", gui)
            break
        except Exception as e:
            consecutive_errors += 1
            print(f"Error: {e}")
            
            if consecutive_errors >= max_consecutive_errors:
                speak("I'm having trouble with repeated errors. Please restart me.", gui)
                break
            else:
                speak("Sorry, something went wrong. Please try again.", gui)
            
            # Small delay to prevent rapid error loops
            time.sleep(1)

def main():
    """Main function to setup GUI and start assistant thread"""
    global gui
    
    print("Starting Jarvis Voice Assistant...")
    print("Available commands:")
    print("- What time is it?")
    print("- What's the weather in [city]?")
    print("- Open recycle bin")
    print("- Empty recycle bin")
    print("- Search for [query]")
    print("- Open [app name]")
    print("- Play [video] on YouTube")
    print("- Open WhatsApp")
    print("- Help")
    print("- Goodbye")
    print("-" * 50)
    
    root = ctk.CTk()
    gui = JarvisGUI(root)

    # Run the assistant logic in a separate thread
    assistant_thread = threading.Thread(target=assistant_thread_func, daemon=True)
    assistant_thread.start()

    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nShutting down Jarvis...")

if __name__ == "__main__":
    main()