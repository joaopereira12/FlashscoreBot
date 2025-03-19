import discord
from discord.ext import commands, tasks
from discord import app_commands
from os import environ
from dotenv import load_dotenv
import asyncio
import os
from itertools import cycle

from cogs.flashscore import LeagueView

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

bot_statuses = cycle(["Serie A", "La Liga", "Liga Portugal", "Premier League"])

@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(bot_statuses)))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    change_status.start()

# class LeagueView(discord.ui.View):

#     def __init__(self, ctx, string: str):
#         super().__init__(timeout=None)
#         self.ctx = ctx
#         self.string = string
       
    
#     @discord.ui.button(label="View League", style=discord.ButtonStyle.primary)
#     async def view_league(self, interaction: discord.Interaction, button: discord.ui.Button):
#         await interaction.response.send_message(self.string, ephemeral=True)

# @bot.command(name="flashscore")
# async def flashscore(ctx):
#     await ctx.send("Hello, World!")

@bot.command(name="test", description="button")
async def button_test(ctx):
    view = LeagueView(ctx, "Ola Manos")
    await ctx.send("ola",view=view)
    
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load()
        await bot.start(token)


load_dotenv()
token = environ['TOKEN']
asyncio.run(main())