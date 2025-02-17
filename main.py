import discord
from discord.ext import commands
from os import environ
from dotenv import load_dotenv
import asyncio
import os

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command(name="hi")
async def hello(ctx):
    await ctx.send("Hello, World!")
    
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load()
        await bot.start(token)


load_dotenv()
token = environ['TOKEN']
asyncio.run(main())