import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from music import Music
from image import Image
from misc import Misc


load_dotenv()

# Get the API token from the .env file.
DISCORD_TOKEN = os.getenv("discord_token")

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print("MIKEBOT RUNNING AND READY")

# Load Cog
bot.add_cog(Music(bot))
bot.add_cog(Image(bot))
bot.add_cog(Misc(bot))

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)