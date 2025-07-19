#!/usr/bin/env python3
# config.py - Enhanced configuration settings and API keys

import os

# OpenWeatherMap API Key
# Sign up at https://openweathermap.org/api to get your free API key
OPENWEATHER_API_KEY = "73c9b7190105d90e2eddd1a4559b142a"

# Speech Recognition Settings
SPEECH_RECOGNITION_CONFIG = {
    'energy_threshold': 300,  # Minimum audio energy to consider for recording
    'dynamic_energy_threshold': True,
    'pause_threshold': 0.8,  # Seconds of non-speaking audio before phrase is complete
    'timeout': 10,  # Maximum seconds to wait for speech
    'phrase_time_limit': 8,  # Maximum seconds for a single phrase
    'language': 'en-US'  # Language for speech recognition
}

# Text-to-Speech Settings
TTS_CONFIG = {
    'rate': 180,  # Speed of speech (words per minute)
    'volume': 1.0,  # Volume level (0.0 to 1.0)
    'voice_index': None  # Voice index (None for default, 0 for first available, 1 for second, etc.)
}

# Application paths - modify for your system
# Format: "app_name": "path/to/executable"
APP_PATHS = {
    # Windows applications
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "code": r"C:\Users\Jitendra Devra\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "vscode": r"C:\Users\Jitendra Devra\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "visual studio code": r"C:\Users\Jitendra Devra\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "cmd": "cmd.exe",
    "powershell": "powershell.exe",
    "task manager": "taskmgr.exe",
    "control panel": "control.exe",
    "file explorer": "explorer.exe",
    "explorer": "explorer.exe",
    
    # Windows Store apps (use protocol handlers)
    "whatsapp": "whatsapp:",
    "microsoft store": "ms-windows-store:",
    "settings": "ms-settings:",
    
    # Multimedia applications
    "vlc": r"C:\Program Files\VideoLAN\VLC\vlc.exe",
    "media player": "wmplayer.exe",
    "spotify": r"C:\Users\{}\AppData\Roaming\Spotify\Spotify.exe".format(os.environ.get('USERNAME', '')),
    
    # Office applications
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
    "outlook": r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE",
    
    # Development tools
    "git bash": r"C:\Program Files\Git\git-bash.exe",
    "github desktop": r"C:\Users\{}\AppData\Local\GitHubDesktop\GitHubDesktop.exe".format(os.environ.get('USERNAME', '')),
    "sublime text": r"C:\Program Files\Sublime Text\sublime_text.exe",
    "atom": r"C:\Users\{}\AppData\Local\atom\atom.exe".format(os.environ.get('USERNAME', '')),
    
    # macOS applications
    "safari": "open -a Safari",
    "terminal": "open -a Terminal",
    "finder": "open -a Finder",
    "chrome": "open -a 'Google Chrome'",
    "firefox": "open -a Firefox",
    "vscode": "open -a 'Visual Studio Code'",
    "code": "open -a 'Visual Studio Code'",
    "xcode": "open -a Xcode",
    "textedit": "open -a TextEdit",
    "preview": "open -a Preview",
    "photoshop": "open -a 'Adobe Photoshop'",
    "illustrator": "open -a 'Adobe Illustrator'",
    
    # Linux applications (using command names)
    "gedit": "gedit",
    "nautilus": "nautilus",
    "firefox": "firefox",
    "chromium": "chromium-browser",
    "libreoffice": "libreoffice",
    "gimp": "gimp",
    "vlc": "vlc",
    "thunderbird": "thunderbird"
}

# Common application aliases for better recognition
APP_ALIASES = {
    "vs code": "code",
    "visual studio code": "code",
    "vscode": "code",
    "google chrome": "chrome",
    "mozilla firefox": "firefox",
    "microsoft edge": "edge",
    "windows explorer": "explorer",
    "file manager": "explorer",
    "command prompt": "cmd",
    "task mgr": "task manager",
    "calc": "calculator",
    "mspaint": "paint",
    "text editor": "notepad",
    "web browser": "chrome",  # Default browser
    "browser": "chrome",
    "music player": "spotify",
    "video player": "vlc",
    "media player": "vlc"
}

# Default cities for weather (when no city is specified)
DEFAULT_CITIES = ["New York", "London", "Tokyo", "Paris", "Sydney"]
DEFAULT_CITY = "New York"

# Debug settings
DEBUG_MODE = True  # Set to False to disable debug output
LOG_COMMANDS = True  # Log all commands for analysis

def get_app_path(app_name):
    """
    Get the application path, checking aliases first
    
    Args:
        app_name (str): Name of the application
        
    Returns:
        str: Path to the application or None if not found
    """
    # Normalize app name
    app_name = app_name.lower().strip()
    
    # Check direct match first
    if app_name in APP_PATHS:
        return APP_PATHS[app_name]
    
    # Check aliases
    if app_name in APP_ALIASES:
        alias_target = APP_ALIASES[app_name]
        if alias_target in APP_PATHS:
            return APP_PATHS[alias_target]
    
    # Check partial matches
    for key in APP_PATHS:
        if app_name in key or key in app_name:
            return APP_PATHS[key]
    
    return None

def validate_config():
    """
    Validate configuration settings and paths
    
    Returns:
        dict: Validation results
    """
    results = {
        'api_key_set': bool(OPENWEATHER_API_KEY and OPENWEATHER_API_KEY != "YOUR_API_KEY_HERE"),
        'valid_apps': [],
        'invalid_apps': [],
        'os_specific_apps': 0
    }
    
    # Check which apps are valid for current OS
    for app_name, app_path in APP_PATHS.items():
        if os.name == 'nt':  # Windows
            if app_path.endswith('.exe') or app_path.startswith('ms-') or ':' in app_path:
                if os.path.exists(app_path) or app_path.endswith('.exe'):
                    results['valid_apps'].append(app_name)
                    results['os_specific_apps'] += 1
                else:
                    results['invalid_apps'].append(app_name)
        else:  # macOS/Linux
            if not app_path.endswith('.exe') and 'ms-' not in app_path:
                results['valid_apps'].append(app_name)
                results['os_specific_apps'] += 1
    
    return results

if __name__ == "__main__":
    # Test configuration when run directly
    print("Jarvis Configuration Validation")
    print("=" * 40)
    
    validation = validate_config()
    
    print(f"API Key configured: {validation['api_key_set']}")
    print(f"Valid apps for {os.name}: {len(validation['valid_apps'])}")
    print(f"Invalid app paths: {len(validation['invalid_apps'])}")
    
    if validation['invalid_apps']:
        print("\nApps with invalid paths:")
        for app in validation['invalid_apps']:
            print(f"  - {app}: {APP_PATHS[app]}")
    
    print(f"\nAvailable commands: {len(validation['valid_apps'])} apps")
    print("Configuration validation complete.")