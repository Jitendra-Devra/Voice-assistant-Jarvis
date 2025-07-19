#!/usr/bin/env python3
# voice_output.py - Handles text-to-speech responses

import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()

# Set properties (optional)
engine.setProperty('rate', 180)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

# Get available voices and set a voice (optional)
voices = engine.getProperty('voices')
# For a female voice (if available)
# engine.setProperty('voice', voices[1].id)

def speak(text, gui): # Add gui as an argument
    """
    Convert text to speech and update the GUI
    
    Args:
        text (str): Text to be spoken
        gui: The GUI object to update
    """
    gui.update_status(f"Jarvis: {text}") # Update GUI instead of printing
    engine.say(text)
    engine.runAndWait()