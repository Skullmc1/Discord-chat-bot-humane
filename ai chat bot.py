import discord
from discord import app_commands
from discord.ext import commands, tasks
import google.generativeai as genai
import random
import time
import asyncio
import sys
import os

try:
    from config import TOKEN, GOOGLE_API_KEY
except ImportError:
    print("Error: config.py file not found")
    input("Press Enter to exit...")
    sys.exit(1)

BOT_RESPONSES = {
    0: [  # Normal
        "I'm at your service!",
        "What do you want master?",
        "I'm here master!",
        "Yes, master?",
        "How can I assist you?"
    ],
    1: [  # Slightly annoyed
        "Yes... what is it now?",
        "*sigh* What do you need?",
        "I'm kinda busy, but go ahead...",
        "Again? Alright, what is it?"
    ],
    2: [  # Irritated
        "This better be important...",
        "You're testing my patience...",
        "*eye roll* What NOW?",
        "Don't you have something better to do?"
    ],
    3: [  # Angry
        "WHAT DO YOU WANT?!",
        "OH MY GOODNESS, WHAT?!",
        "FOR THE LOVE OF... WHAT?!",
        "CAN YOU NOT?!"
    ]
}


# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Set up bot with all intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Track user pings and conversations
user_pings = {}  # {user_id: {'count': int, 'last_ping': timestamp}}
PING_TIMEOUT = 60

def check_config():
    if TOKEN == 'ENTER YOUR DISCORD BOT TOKEN HERE' or not TOKEN:
        print("Please add your Discord bot token to config.py")
        input("Press Enter to exit...")
        sys.exit(1)
    if GOOGLE_API_KEY == 'ENTER YOUR GOOGLE API KEY HERE' or not GOOGLE_API_KEY:
        print("Please add your Google API key to config.py")
        input("Press Enter to exit...")
        sys.exit(1)

check_config()

async def get_ai_response(prompt, anger_level):
    try:
        # Create a context-aware prompt based on anger level
        context = f"Roleplay as a boy. Don't let them think you are an AI. You should act dumb to most questions. You have an anger level of {anger_level}/5. "
        context += "If anger level is 0, be helpful and polite. "
        context += "If anger level is 1, be slightly annoyed. "
        context += "If anger level is 2, be irritated. "
        context += "If anger level is 3, be very angry. "
        context += "If anger level is 4, be extremely angry. "
        context += "If anger level is 5, be furious. "
        context += "Never break character. Don't append anger level to your responses. "
        context += f"Respond to: {prompt}"

        response = model.generate_content(context)
        return response.text
    except Exception as e:
        print(f"AI Error: {e}")
        # Fallback to default responses if AI fails
        return random.choice(BOT_RESPONSES[anger_level])

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
        
    if bot.user.mentioned_in(message):
        current_time = time.time()
        user_id = message.author.id
        
        # Clean up old entries and manage anger level
        for uid in list(user_pings.keys()):
            if current_time - user_pings[uid]['last_ping'] > PING_TIMEOUT:
                del user_pings[uid]
        
        if user_id not in user_pings:
            user_pings[user_id] = {'count': 0, 'last_ping': current_time}
        else:
            if current_time - user_pings[user_id]['last_ping'] > PING_TIMEOUT:
                user_pings[user_id] = {'count': 0, 'last_ping': current_time}
            else:
                user_pings[user_id]['count'] += 1
                user_pings[user_id]['last_ping'] = current_time
        
        anger_level = min(user_pings[user_id]['count'] // 2, 3)
        
        # Get user's message content without the mention
        user_message = message.content.replace(f'<@{bot.user.id}>', '').strip()
        if not user_message:
            user_message = "Hi"

        # Add typing indicator
        async with message.channel.typing():
            if anger_level >= 2:
                await asyncio.sleep(1)  # Dramatic pause for angry responses
            
            # Get AI response
            response = await get_ai_response(user_message, anger_level)
            await message.reply(response)
    
    await bot.process_commands(message)

# ... rest of your existing code ...
bot.run(TOKEN)