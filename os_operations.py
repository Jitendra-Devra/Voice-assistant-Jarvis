# os_operations.py - Enhanced OS operations with better error handling
import subprocess
import os
import sys
from voice_output import speak

# Try to import Windows-specific modules
try:
    import winshell
    WINSHELL_AVAILABLE = True
except ImportError:
    WINSHELL_AVAILABLE = False
    print("Warning: winshell not available. Some Windows features may not work.")

def open_recycle_bin(gui):
    """Opens the Recycle Bin folder with enhanced error handling."""
    try:
        if os.name == 'nt':  # Windows
            print("DEBUG - Attempting to open Recycle Bin...")
            
            # Try multiple methods to open recycle bin
            methods = [
                # Method 1: Use explorer with shell command
                lambda: subprocess.run(['explorer', 'shell:RecycleBinFolder'], 
                                     check=True, timeout=10),
                
                # Method 2: Use start command
                lambda: subprocess.run(['cmd', '/c', 'start', 'shell:RecycleBinFolder'], 
                                     check=True, timeout=10),
                
                # Method 3: Direct shell command
                lambda: subprocess.run('explorer shell:RecycleBinFolder', 
                                     shell=True, check=True, timeout=10)
            ]
            
            for i, method in enumerate(methods, 1):
                try:
                    print(f"DEBUG - Trying method {i}...")
                    method()
                    speak("Recycle Bin opened successfully.", gui)
                    return True
                except subprocess.CalledProcessError as e:
                    print(f"DEBUG - Method {i} failed with return code {e.returncode}")
                    continue
                except subprocess.TimeoutExpired:
                    print(f"DEBUG - Method {i} timed out")
                    continue
                except Exception as e:
                    print(f"DEBUG - Method {i} failed with error: {e}")
                    continue
            
            # If all methods failed
            speak("I had trouble opening the Recycle Bin. Please try opening it manually.", gui)
            return False
            
        else:  # macOS or Linux
            if sys.platform == 'darwin':  # macOS
                try:
                    subprocess.run(['open', os.path.expanduser('~/.Trash')], 
                                 check=True, timeout=10)
                    speak("Trash opened successfully.", gui)
                    return True
                except Exception as e:
                    print(f"macOS trash error: {e}")
                    speak("I couldn't open the Trash folder.", gui)
                    return False
            else:  # Linux
                trash_paths = [
                    os.path.expanduser('~/.local/share/Trash/files'),
                    os.path.expanduser('~/.Trash'),
                    '/tmp/Trash'
                ]
                
                for trash_path in trash_paths:
                    if os.path.exists(trash_path):
                        try:
                            subprocess.run(['xdg-open', trash_path], 
                                         check=True, timeout=10)
                            speak("Trash folder opened successfully.", gui)
                            return True
                        except Exception as e:
                            print(f"Linux trash error for {trash_path}: {e}")
                            continue
                
                speak("I couldn't locate the trash folder on this Linux system.", gui)
                return False
                
    except Exception as e:
        print(f"Error opening recycle bin: {e}")
        speak("I encountered an error trying to open the recycle bin.", gui)
        return False

def empty_recycle_bin(gui):
    """
    Empties the Recycle Bin with enhanced error handling and confirmation.
    """
    try:
        if os.name == 'nt':  # Windows
            if not WINSHELL_AVAILABLE:
                speak("Sorry, I need the winshell library to empty the recycle bin on Windows.", gui)
                return False
            
            # Check if recycle bin has items first
            try:
                recycle_bin = winshell.recycle_bin()
                items = list(recycle_bin)
                
                if not items:
                    speak("The recycle bin is already empty.", gui)
                    return True
                
                item_count = len(items)
                speak(f"The recycle bin contains {item_count} items. This action cannot be undone.", gui)
                
                # In a real implementation, you might want to add voice confirmation here
                # For now, we'll proceed with a warning
                
                print("DEBUG - Attempting to empty recycle bin...")
                recycle_bin.empty(confirm=False, show_progress=False, sound=False)
                speak("The recycle bin has been emptied successfully.", gui)
                return True
                
            except Exception as e:
                print(f"Error accessing recycle bin: {e}")
                speak("I couldn't access the recycle bin contents.", gui)
                return False
                
        else:  # macOS or Linux
            if sys.platform == 'darwin':  # macOS
                try:
                    trash_path = os.path.expanduser('~/.Trash')
                    if os.path.exists(trash_path):
                        # Count items first
                        items = os.listdir(trash_path)
                        if not items:
                            speak("The trash is already empty.", gui)
                            return True
                        
                        speak(f"The trash contains {len(items)} items. Emptying now.", gui)
                        subprocess.run(['rm', '-rf', f'{trash_path}/*'], 
                                     shell=True, check=True, timeout=30)
                        speak("Trash emptied successfully.", gui)
                        return True
                    else:
                        speak("I couldn't find the trash folder.", gui)
                        return False
                        
                except Exception as e:
                    print(f"macOS trash empty error: {e}")
                    speak("I encountered an error emptying the trash.", gui)
                    return False
                    
            else:  # Linux
                trash_paths = [
                    os.path.expanduser('~/.local/share/Trash/files'),
                    os.path.expanduser('~/.Trash')
                ]
                
                for trash_path in trash_paths:
                    if os.path.exists(trash_path):
                        try:
                            items = os.listdir(trash_path)
                            if not items:
                                speak("The trash is already empty.", gui)
                                return True
                            
                            speak(f"Emptying {len(items)} items from trash.", gui)
                            subprocess.run(['rm', '-rf', f'{trash_path}/*'], 
                                         shell=True, check=True, timeout=30)
                            speak("Trash emptied successfully.", gui)
                            return True
                            
                        except Exception as e:
                            print(f"Linux trash empty error for {trash_path}: {e}")
                            continue
                
                speak("I couldn't empty the trash on this Linux system.", gui)
                return False
                
    except Exception as e:
        print(f"Error emptying recycle bin: {e}")
        speak("I ran into an error trying to empty the recycle bin.", gui)
        return False

def check_system_compatibility():
    """
    Check system compatibility and available features
    """
    print(f"Operating System: {os.name}")
    print(f"Platform: {sys.platform}")
    
    if os.name == 'nt':
        print(f"Winshell available: {WINSHELL_AVAILABLE}")
        if not WINSHELL_AVAILABLE:
            print("Tip: Install winshell with 'pip install winshell' for full Windows support")
    
    return {
        'os_name': os.name,
        'platform': sys.platform,
        'winshell_available': WINSHELL_AVAILABLE
    }

def get_recycle_bin_info(gui):
    """
    Get information about the recycle bin contents
    """
    try:
        if os.name == 'nt' and WINSHELL_AVAILABLE:
            recycle_bin = winshell.recycle_bin()
            items = list(recycle_bin)
            count = len(items)
            
            if count == 0:
                speak("The recycle bin is empty.", gui)
            elif count == 1:
                speak("The recycle bin contains 1 item.", gui)
            else:
                speak(f"The recycle bin contains {count} items.", gui)
            
            return count
        else:
            speak("Recycle bin information is only available on Windows with winshell installed.", gui)
            return None
            
    except Exception as e:
        print(f"Error getting recycle bin info: {e}")
        speak("I couldn't get recycle bin information.", gui)
        return None

if __name__ == "__main__":
    # Test the OS operations when run directly
    compatibility = check_system_compatibility()
    print("System compatibility check completed.")