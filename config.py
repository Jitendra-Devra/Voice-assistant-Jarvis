#!/usr/bin/env python3
# config.py - Configuration settings and API keys

# OpenWeatherMap API Key
# Sign up at https://openweathermap.org/api to get your free API key
OPENWEATHER_API_KEY ="73c9b7190105d90e2eddd1a4559b142a"

# Application paths - modify for your system
# Format: "app_name": "path/to/executable"
APP_PATHS = {
    # Windows examples
    "notepad": "notepad.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "code": r"C:\Users\Jitendra Devra\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    
    # Windows Store WhatsApp (no need for path since we use protocol handler)
    "whatsapp": "whatsapp:",
    
    # macOS examples
    "safari": "open -a Safari",
    "terminal": "open -a Terminal",
    "finder": "open -a Finder",
    
    # Add your custom applications here
    # "app_name": "path/to/app", 
}