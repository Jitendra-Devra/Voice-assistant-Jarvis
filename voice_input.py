#!/usr/bin/env python3
# voice_input.py - Enhanced microphone input and speech-to-text conversion

import speech_recognition as sr
import time

def listen_for_command(gui):
    """
    Listen for a voice command and convert it to text with improved error handling
    
    Returns:
        str: The recognized text command or empty string if not recognized
    """
    recognizer = sr.Recognizer()
    
    # More sensitive microphone settings for better recognition
    recognizer.energy_threshold = 4000  # Increased from 300 for better noise filtering
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 1.2  # Increased from 0.8 to allow for natural pauses
    recognizer.operation_timeout = None  # No timeout for listening
    
    try:
        with sr.Microphone() as source:
            # Update GUI status
            gui.update_status("Adjusting for ambient noise...")
            
            # Adjust for ambient noise with a longer duration for better accuracy
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=2.0)  # Increased duration
            print(f"Energy threshold set to: {recognizer.energy_threshold}")
            
            gui.update_status("Listening...")
            gui.start_listening_animation()
            
            print("Listening for command... (Speak now)")
            
            # Listen for the user's input with improved settings
            try:
                # Increased timeouts for better recognition
                audio = recognizer.listen(source, timeout=15, phrase_time_limit=10)
                
                gui.update_status("Processing speech...")
                gui.stop_listening_animation()
                
                print("Audio captured, processing...")
                
                # Use Google's speech recognition with improved error handling
                try:
                    # Try Google Speech Recognition first
                    command = recognizer.recognize_google(audio, language='en-US')
                    print(f"Recognized: '{command}'")
                    gui.update_status("Ready")
                    return command.lower()
                    
                except sr.UnknownValueError:
                    print("Could not understand audio")
                    gui.update_status("Could not understand - please try again")
                    # Try with different language settings if first attempt fails
                    try:
                        command = recognizer.recognize_google(audio, language='en-IN')
                        print(f"Recognized (en-IN): '{command}'")
                        gui.update_status("Ready")
                        return command.lower()
                    except:
                        time.sleep(1)
                        gui.update_status("Ready")
                        return ""
                    
                except sr.RequestError as e:
                    print(f"Google Speech Recognition error: {e}")
                    gui.update_status("Speech service error - please try again")
                    speak_safe("Sorry, speech recognition service is unavailable.", gui)
                    return ""
                        
            except sr.WaitTimeoutError:
                print("Listening timeout - no speech detected")
                gui.stop_listening_animation()
                gui.update_status("No speech detected - ready for next command")
                # Don't speak timeout errors to avoid audio feedback loops
                return ""
                
    except OSError as e:
        print(f"Microphone error: {e}")
        gui.update_status("Microphone error - check your audio device")
        speak_safe("There seems to be a problem with the microphone. Please check your audio device.", gui)
        return ""
        
    except Exception as e:
        print(f"Unexpected error in listen_for_command: {e}")
        gui.update_status("Audio processing error")
        gui.stop_listening_animation()
        return ""

def speak_safe(text, gui):
    """
    Safe speak function that handles import errors
    """
    try:
        from voice_output import speak
        speak(text, gui)
    except ImportError:
        print(f"Voice output not available: {text}")
        gui.update_status(f"Jarvis: {text}")

def test_microphone():
    """
    Test microphone functionality with better debugging
    """
    recognizer = sr.Recognizer()
    
    print("Testing microphone...")
    print("Available microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"  {index}: {name}")
    
    try:
        # Try with default microphone first
        with sr.Microphone() as source:
            print("Default microphone found. Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=3)  # Longer adjustment
            print(f"Energy threshold: {recognizer.energy_threshold}")
            print("Say something to test the microphone (you have 10 seconds):")
            
            try:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                print("Audio captured successfully!")
                
                try:
                    result = recognizer.recognize_google(audio, language='en-US')
                    print(f"Recognition test successful: '{result}'")
                    return True
                except sr.UnknownValueError:
                    print("Audio captured but could not understand speech. This might be normal.")
                    return True  # Mic works, just couldn't understand
                except sr.RequestError as e:
                    print(f"Recognition service error: {e}")
                    return False
            except sr.WaitTimeoutError:
                print("No speech detected within timeout period")
                print("Microphone hardware seems to work, but no speech was detected.")
                print("Try speaking louder or closer to the microphone.")
                return True  # Mic hardware works
                
    except OSError as e:
        print(f"Microphone not found or accessible: {e}")
        print("Possible solutions:")
        print("1. Check if your microphone is plugged in")
        print("2. Make sure microphone permissions are enabled")
        print("3. Try running as administrator")
        return False
    except Exception as e:
        print(f"Microphone test failed: {e}")
        return False

def list_microphones():
    """List all available microphones"""
    print("Available microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"  {index}: {name}")

if __name__ == "__main__":
    # List available microphones
    list_microphones()
    print("-" * 50)
    
    # Test the microphone when run directly
    if test_microphone():
        print("Microphone test passed!")
    else:
        print("Microphone test failed. Please check your audio settings.")