import discord
from discord.ext import commands
from tabulate import tabulate
from scraper import *

class TeamInfoButton(discord.ui.Button):
    def __init__(self, country, league, team):
        super().__init__(label=f"View {team}", style=discord.ButtonStyle.secondary)
        self.team = team
        self.country = country
        self.league = league

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        print(f"🔍 Fetching team info for {self.team} in {self.league}")

        try:
            team_details = team_info(self.country, self.league, self.team)  # Ensure function exists
            print(f"✅ Team Info Retrieved: {team_details}")

            prev_matches_text = ""
            for match_date, home, away, home_score, away_score in team_details["prev_matches"]:
                prev_matches_text += f"{match_date} {home} {home_score} - {away_score} {away}\n"

            next_matches_text = ""
            for match_date, home, away in team_details["next_matches"]:
                next_matches_text += f"{match_date} {home} vs {away}\n"

            embed = discord.Embed(title=f"🔍 {self.team}", color=discord.Color.blue())
            embed.add_field(name="📅 Previous Matches", value=f"\n{prev_matches_text}\n", inline=False)
            embed.add_field(name="📅 Next Matches", value=f"\n{next_matches_text}\n", inline=False)
            embed.set_footer(text="Powered by Flashscore ⚽")

            view = discord.ui.View()
            view.add_item(LeagueSelection()) 

            # ✅ Use `followup.send` instead of `edit`, so it doesn’t replace standings.
            await interaction.followup.send(embed=embed, view=view)  

        except Exception as e:
            print(f"🚨 Error fetching team info: {e}")
            await interaction.followup.send("❌ Failed to retrieve team info.", ephemeral=True)

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
            
            print("⚡ Interaction received!")  # ✅ Log the interaction
            await interaction.response.defer()  # ✅ Acknowledge the interaction

            country, league = self.values[0].split(";")  
            print(f"🌍 Selected Country: {country}, League: {league}")  # ✅ Log selection

            # ✅ Send a temporary "Loading..." message
            loading_message = await interaction.followup.send("⏳ Loading league data, please wait...", ephemeral=False)

            try:
                # ✅ Fetch last results
                last_results = last_results_league(country, league)
                print(f"📊 Fetched Last Results: {last_results}")

                last_results_text = ""
                for round_name, matches in last_results.items():
                    last_results_text += f"\n⚽ **{round_name}**\n"
                    for event_time, home_team, away_team, home_score, away_score in matches:
                        last_results_text += f"{home_team} {home_score} - {away_score} {away_team} ({event_time})\n"

                    if len(last_results_text) > 950:  
                        last_results_text += "... (more matches not displayed)\n"
                        break

                # ✅ Fetch upcoming fixtures
                next_fixtures = league_next_fixtures(country, league)
                print(f"📊 Fetched Next Fixtures: {next_fixtures}")

                next_fixtures_text = ""
                for round_name, matches in next_fixtures.items():
                    next_fixtures_text += f"\n⚽ **{round_name}**\n"
                    for event_time, home_team, away_team in matches:
                        next_fixtures_text += f"{home_team} - {away_team} ({event_time})\n"

                    if len(next_fixtures_text) > 950:  
                        next_fixtures_text += "... (more matches not displayed)\n"
                        break

                # ✅ Fetch standings
                standings = league_standings(country, league)
                print(f"📊 Fetched Standings: {standings}")

                if not standings:
                    raise ValueError("❌ No standings found!")

                # ✅ Format standings table
                table = tabulate(
                    standings, 
                    headers=["Team", "G", "W", "D", "L", "GD", "P"], 
                    tablefmt=""
                )

                # ✅ Create the final embed
                embed = discord.Embed(title=f"🏆 {league.replace('-', ' ').title()}", color=discord.Color.blue())
                embed.add_field(name="📅 Last Round Results", value=f"\n\n{last_results_text}\n", inline=False)
                embed.add_field(name="📅 Next Fixtures", value=f"\n\n{next_fixtures_text}\n", inline=False)
                embed.description = f"\n📊 **Standings**\n```\n{table}\n```"
                embed.set_footer(text="Powered by Flashscore ⚽")

                # ✅ Add buttons for each team
                view = discord.ui.View()
                view.add_item(LeagueSelection())  # Keep the dropdown menu
                for team, *_ in standings:  
                    view.add_item(TeamInfoButton(country, league, team))

                # ✅ Edit the original "Loading..." message with the final embed
                await loading_message.edit(content=None, embed=embed, view=view)

            except Exception as e:
                print(f"🚨 Error: {e}")
                await loading_message.edit(content="❌ Failed to retrieve standings. Try again later.", embed=None, view=None)

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