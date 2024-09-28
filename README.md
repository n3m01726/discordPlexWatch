# Plex Status Watcher Discord Bot

This is a Discord bot that monitors the status of a Plex server and provides updates in a specified Discord channel. It also allows users to check the server status manually and make special requests, with OMBI.

## Features

- **Plex Server Monitoring**: Automatically checks the status of a Plex server every 5 minutes.
- **Discord Integration**: Sends updates to a specified Discord channel about the Plex server status (Online/Offline).
- **Manual Status Check**: Users can check the current status of the Plex server with the `!status` command.
- **Request Feature**: Users can make special requests through the `!request` command, which provides a link to the request page.

## Requirements

- Python 3.8 or higher
- `discord.py` library
- `requests` library
- `python-dotenv` library

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/n3m01726/discordPlexWatch.git
   cd <repository-directory>
   ```
2. Install the required packages:
3. Create a .env file in the project directory and add your Discord and Plex credentials:
   ```bash
    DISCORD_TOKEN=<your-discord-bot-token>
    PLEX_SERVER_URL=<your-plex-server-url>
    PLEX_TOKEN=<your-plex-token>
    STATUS_CHANNEL_ID=<discord-channel-id>
    ```

4. To run the bot, execute the following command: python main.py

## Commands
- <code>!status</code>: Check the current status of the Plex server.
- <code>!request</code>: Get a link to make a special request.

## Logging
All bot activity is logged to a file named <code>logs.txt</code>.

## License
This project is licensed under the MIT License.

   
