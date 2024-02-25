import disnake
from disnake.ext import commands
import config

db = config.db
cur = config.cur

class Rewards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="rewards", description="Check out the rewards!")
    async def rewards(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.send_message("Please wait...", ephemeral=True)
        cur.execute("SELECT * FROM user_stats WHERE user_id = %s", (str(interaction.user.id),))
        if not cur.fetchone():
            await interaction.response.send_message("Whoops! Seems like you have not created a room yet! Create it first then try to use this command again.")
            return

        embed = disnake.Embed(title="Rewards...")
        for item in config.items:
            embed.add_field(name=f"{item[0]} (Requires level {item[3]})", value=f"{item[1]} **(Multiplies xp by {item[2]}x)**\n", inline=False)
        await interaction.edit_original_response(embed=embed, content="")
        return

def setup(bot: commands.Bot):
    bot.add_cog(Rewards(bot))