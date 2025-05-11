# Jarvis - Voice-Based Virtual Assistant

A simple, Python-based voice assistant named Jarvis that listens to voice commands and performs various actions.

## Features

- **Voice Input**: Converts speech to text using Google Speech API
- **Voice Output**: Responds with natural-sounding speech
- **Google Search**: Opens search results in your default browser
- **YouTube**: Opens and searches for videos on YouTube
- **WhatsApp**: Opens WhatsApp Web in your browser
- **Weather Reports**: Gets current weather for any city
- **Time Reporting**: Tells you the current time
- **App Launching**: Opens applications on your computer

## Setup and Installation

### Prerequisites

- Python 3.6 or higher
- Working microphone
- Internet connection (for speech recognition and weather data)

### Installation

1. Clone or download this repository
2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. PyAudio installation:
   - Windows: `pip install PyAudio`
   - macOS: `brew install portaudio` then `pip install PyAudio`
   - Linux: `sudo apt-get install python3-pyaudio` or `pip install PyAudio`

4. Get an OpenWeatherMap API key:
   - Sign up at [OpenWeatherMap](https://openweathermap.org/api)
   - Copy your API key
   - Open `config.py` and replace `YOUR_API_KEY_HERE` with your actual API key

5. Configure application paths in `config.py` to match your system

### Running the Assistant

```bash
python main.py
```

## How to Use

After starting the assistant:

1. Wait for the "Listening..." prompt
2. Speak a command clearly, for example:
   - "What time is it?"
   - "What's the weather in London?"
   - "Search for Python programming tutorials"
   - "Open Chrome"
   - "Play music on YouTube"
   - "Open WhatsApp"
   - "Goodbye" (to exit)

## Project Structure

- `main.py`: Main program loop and command processing
- `voice_input.py`: Handles microphone input and speech-to-text
- `voice_output.py`: Handles text-to-speech responses
- `commands.py`: Contains functions for each command type
- `config.py`: Configuration settings and API keys

## Troubleshooting

- **Microphone not working**: Make sure your microphone is set as the default device
- **"Could not understand audio"**: Speak more clearly or check your microphone
- **Weather API errors**: Verify your API key in `config.py`
- **App won't launch**: Update the correct path in `config.py`

## Future Enhancements

- Wake word detection
- Timer and reminder functionality
- Email integration
- Natural language processing for better command understanding
- Custom chatbot integration