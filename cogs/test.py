import discord
from discord.ext import commands

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online")
    
    @commands.command(name="send")
    async def sendEmbed(self, ctx):
        embeded_msg = discord.Embed(title="Embed", description="description", color=discord.Color.green())
        embeded_msg.set_thumbnail(url=ctx.author.avatar)
        embeded_msg.add_field(name="Name of field", value = "Value of field", inline=False)
        embeded_msg.set_image(url=ctx.guild.icon)
        embeded_msg.set_footer(text="footer text", icon_url=ctx.author.avatar)
        await ctx.send(embed=embeded_msg)