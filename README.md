# Discord AI Chat Bot

A Discord bot powered by Google's Gemini AI that simulates human-like conversations with dynamic personality shifts. The bot becomes progressively more irritated when pinged repeatedly, creating a more realistic interaction experience.

## Features
- 🤖 Powered by Google's Gemini-Pro AI model
- 😊 Dynamic personality system that changes based on interaction frequency
- 🎭 Roleplays as a human character, maintaining consistent personality
- ⏲️ Timeout system to reset bot's "mood" after periods of inactivity
- 💬 Natural conversation handling with context awareness

## Prerequisites
- Python 3.8+
- Discord Bot Token
- Google API Key (Gemini)

## Setup
1. Clone this repository
2. Create a `config.py` file in the root directory with:

```python
TOKEN = "YOUR_DISCORD_BOT_TOKEN"
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
```

## Installation
```bash
pip install discord.py google-generativeai
```

## Usage
- Mention the bot to start a conversation
- Bot's responses become more irritated with repeated pings
- Timeout resets the bot's mood, allowing for a fresh conversation

## Contributing
- Contributions are welcome! Please open an issue or submit a pull request.
