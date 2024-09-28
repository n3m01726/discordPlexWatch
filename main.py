import os
import discord
import requests
import asyncio
import aiohttp
import logging
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Charger les configurations depuis les variables d'environnement
PLEX_SERVER_URL = os.getenv("PLEX_SERVER_URL")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Configuration des logs
logging.basicConfig(filename='log.txt',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def check_plex_server():
    await client.wait_until_ready()
    channel = client.get_channel(DISCORD_CHANNEL_ID)

    plex_down = False

    async with aiohttp.ClientSession() as session:
        while not client.is_closed():
            try:
                async with session.get(PLEX_SERVER_URL, timeout=5) as response:
                    if response.status == 200:
                        if plex_down:
                            await channel.send("😀 Plex server is back up!")
                        plex_down = False
                        logging.info("Plex server is up.")
                    else:
                        if not plex_down:
                            await channel.send(
                                "⚠️ Plex server is down or unreachable!")
                        plex_down = True
                        logging.warning("Plex server seems down.")
            except aiohttp.ClientError as e:
                if not plex_down:
                    await channel.send("⚠️ Plex server is down or unreachable!"
                                       )
                plex_down = True
                logging.error(f"Error reaching Plex server: {e}")

            await asyncio.sleep(300)


@client.event
async def on_ready():
    logging.info(f'Logged in as {client.user}')
    client.loop.create_task(check_plex_server())


# Démarrer le bot
client.run(DISCORD_TOKEN)
