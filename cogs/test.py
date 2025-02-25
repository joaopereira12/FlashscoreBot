import discord
from discord.ext import commands

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online")
    
    @commands.command()
    async def send(self, ctx):
        embeded_msg = discord.Embed(title="Embed", description="description", color=discord.Color.green())
        embeded_msg.set_thumbnail(url=ctx.author.avatar.url)
        embeded_msg.add_field(name="Name of field", value = "Value of field", inline=False)
        embeded_msg.set_image(url=ctx.guild.icon)
        embeded_msg.set_footer(text="footer text", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embeded_msg)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

async def setup(bot):
    await bot.add_cog(Test(bot))