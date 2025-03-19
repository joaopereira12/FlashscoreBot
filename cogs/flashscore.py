import discord
from discord.ext import commands
from tabulate import tabulate
from scraper import *

class TeamInfoButton(discord.ui.Button):
    def __init__(self, team_name):
        super().__init__(label=f"View {team_name}", style=discord.ButtonStyle.secondary)
        self.team_name = team_name

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        team_info = f"🔍 Details for **{self.team_name}**:\n⚽ More information coming soon!"
        await interaction.followup.send(team_info, ephemeral=True) 

class LeagueSelection(discord.ui.Select):

        def __init__(self):
            options = [
                discord.SelectOption(label="Serie A", value="italia;serie-a", description="Italian top division"),
                discord.SelectOption(label="La Liga", value="espanha;laliga", description="Spanish top division"),
                discord.SelectOption(label="Premier League", value="inglaterra;premier-league", description="English top division"),
                discord.SelectOption(label="Bundesliga", value="alemanha;bundesliga", description="German top division"),
                discord.SelectOption(label="Ligue 1", value="franca;ligue-1", description="French top division"),
                discord.SelectOption(label="Liga Portugal Betclic", value="portugal;liga-portugal-betclic", description="Portuguese top division")
            ]
            super().__init__(placeholder="Select a league", options=options)

        async def callback(self, interaction: discord.Interaction):
            
            print("⚡ Interaction received!")  # ✅ Check if interaction is received
            await interaction.response.defer()

            country, league = self.values[0].split(";")  
            print(f"🌍 Selected Country: {country}, League: {league}")  # ✅ Log selection

            try:
                last_results = last_results_league(country, league)
                print(f"📊 Fetched Last Results: {last_results}")

                # ✅ Format the last results (compact format)
                last_results_text = ""

                for round_name, matches in last_results.items():
                    last_results_text += f"⚽ **{round_name}**\n"
                    for event_time, home_team, away_team, home_score, away_score in matches:
                        last_results_text += f"{home_team} {home_score} - {away_score} {away_team} ({event_time})\n"

                    if len(last_results_text) > 950:  # ✅ Ensure it doesn't exceed Discord's limit (1024 per field)
                        last_results_text += "... (more matches not displayed)\n"
                        break

                next_fixtures = league_next_fixtures(country, league)
                print(f"📊 Fetched Last Results: {last_results}")

                # ✅ Format the last results (compact format)
                next_fixtures_text = ""

                for round_name, matches in next_fixtures.items():
                    next_fixtures_text += f"⚽ **{round_name}**\n"
                    for event_time, home_team, away_team in matches:
                        next_fixtures_text += f"{home_team} - {away_team} ({event_time})\n"

                    if len(next_fixtures_text) > 950:  # ✅ Ensure it doesn't exceed Discord's limit (1024 per field)
                        next_fixtures_text += "... (more matches not displayed)\n"
                        break

                standings = league_standings(country, league)  # Fetch data
                print(f"📊 Fetched Standings: {standings}")  # ✅ Log data

                if not standings:  
                    raise ValueError("❌ No standings found!")

                # Format table
                table = tabulate(
                    standings, 
                    headers=["Team", "G", "W", "D", "L", "GD", "P"], 
                    tablefmt=""
                )

                # Create Embed
                embed = discord.Embed(title=f"🏆 {league.replace('-', ' ').title()}", color=discord.Color.blue())
                embed.add_field(name="📅 Last Round Results", value=f"```\n{last_results_text}\n```", inline=False)
                embed.add_field(name="📅 Next Fixtures", value=f"```\n{next_fixtures_text}\n```", inline=False)
                embed.add_field(name="📊 Standings", value=f"```\n{table}\n```", inline=False)
                embed.set_footer(text="Powered by Flashscore ⚽")

                view = discord.ui.View()
                for team, *_ in standings:  # Iterate over teams and create buttonsa
                    view.add_item(TeamInfoButton(team))
                
                # ✅ Edit the original message instead of sending a new one
                await interaction.message.edit(embed=embed, view=view)

            except Exception as e:
                print(f"🚨 Error: {e}")
                await interaction.followup.send("❌ Failed to retrieve standings. Try again later.", ephemeral=True)

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