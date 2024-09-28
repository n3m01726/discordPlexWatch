import os
import discord
from discord.ext import tasks, commands
import requests
import logging
from datetime import datetime
import pytz
from dotenv import load_dotenv

load_dotenv()

# Logging configuration
logging.basicConfig(filename='logs.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True  # Enable privileged message content intent
bot = commands.Bot(command_prefix='!', intents=intents)

# Plex server details
PLEX_SERVER_URL = os.getenv('PLEX_SERVER_URL')
PLEX_TOKEN = os.getenv('PLEX_TOKEN')
STATUS_CHANNEL_ID = int(os.getenv('STATUS_CHANNEL_ID'))

status_message = None  # To store the status message
plex_down = True  # To track the status of the Plex server

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await check_plex_server.start()  # Start the Plex server checking task

@tasks.loop(minutes=5)  # Check every 5 minutes
async def check_plex_server():
    global status_message, plex_down

    try:
        response = requests.get(PLEX_SERVER_URL, headers={'X-Plex-Token': PLEX_TOKEN})
        channel = bot.get_channel(STATUS_CHANNEL_ID)

        if response.status_code == 200:  # If the server is online
            if plex_down:  # If the server was offline and is now back online
                plex_down = False
                await channel.send("😀 Plex server is back up!")  # Unique notification for coming online
                if status_message:
                    await status_message.delete()  # Delete the old status message
                status_message = await channel.send("🟢 Plex server status: Online")  # Update the status message
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="to Plex server: Status: Online"))  # Update bot status
                logging.info("Plex server is up.")
        else:  # If the server is offline
            if not plex_down:  # If the server was online and is now offline
                plex_down = True
                if status_message:
                    await status_message.delete()  # Delete the old status message
                status_message = await channel.send("🔴 Plex server status: Offline")  # Update the status message
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="to Plex server: Status: Offline"))  # Update bot status
                logging.info("Plex server is down.")
    except Exception as e:
        logging.error(f"Error checking Plex server: {e}")

@bot.command()
async def status(ctx):
    """Check the current status of the Plex server."""
    if plex_down:
        await ctx.send("🔴 Plex server status: Offline")
    else:
        await ctx.send("🟢 Plex server status: Online")

@bot.command()
async def request(ctx):
    """Provide a link to make a special request."""
    await ctx.send("To make a special request, please visit: [Ombi Link Here]")

bot.run(os.getenv('DISCORD_TOKEN'))
