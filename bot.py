import asyncio
import discord
from discord.ext import commands
from config import DISCORD_BOT_TOKEN
import os

intents = discord.Intents.default()
intents.typing = False
intents.presences = True
intents.message_content = True


async def main():
    print(f"Starting Skali Bot...")
    bot = commands.Bot(command_prefix=";", intents=intents)
    async with bot:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")
        await bot.start(DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
