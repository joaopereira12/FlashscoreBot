import discord
from discord.ext import commands

class LeagueSelection(discord.ui.Select):

        def __init__(self):
            options = [
                discord.SelectOption(label="Serie A", description="Italian top division"),
                discord.SelectOption(label="La Liga", description="Spanish top division"),
                discord.SelectOption(label="Premier League", description="English top division"),
                discord.SelectOption(label="Bundesliga", description="German top division"),
                discord.SelectOption(label="Ligue 1", description="French top division"),
                discord.SelectOption(label="Liga Portugal Betclic", description="Portuguese top division")
            ]
            super().__init__(placeholder="Select a league", options=options)

        async def callback(self, interaction: discord.Interaction):
            embed = discord.Embed(
                title="League Selection",
                description=f"You selected **{self.values[0]}**",
                color=discord.Color.blue()
            )
            embed.set_footer(text="Powered by Flashscore ⚽")
            await interaction.response.send_message(embed=embed, ephemeral=True)

class LeagueView(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.add_item(LeagueSelection())

class Flashscore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="flashscore")
    async def flashscore(self, ctx):
        view = LeagueView()

        embed = discord.Embed(
            title="Football Leagues",
            description="Select a league from the dropdown below!",
            color=discord.Color.green()
        )
        embed.set_footer(text="Powered by Flashscore ⚽")

        await ctx.send(embed=embed, view=view)
    

async def setup(bot):
    await bot.add_cog(Flashscore(bot))