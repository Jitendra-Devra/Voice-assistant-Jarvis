#!/usr/bin/env python3
# voice_input.py - Handles microphone input and speech-to-text conversion

import speech_recognition as sr

def listen_for_command():
    """
    Listen for a voice command and convert it to text
    
    Returns:
        str: The recognized text command or empty string if not recognized
    """
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        # Listen for the user's input
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("Processing speech...")
            
            # Use Google's speech recognition
            try:
                command = recognizer.recognize_google(audio)
                return command
            except sr.UnknownValueError:
                print("Could not understand audio")
                return ""
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return ""
                
        except sr.WaitTimeoutError:
            print("Listening timed out")
            return ""