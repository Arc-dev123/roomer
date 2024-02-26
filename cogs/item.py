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
            embed.add_field(name=f"{item[0]} (Requires level {item[3]})", value=f"{item[1]} **(Multiplies xp by {item[2]}x)**", inline=False)
        await interaction.edit_original_response(embed=embed, content="")
        return

    @commands.slash_command(name="claim", description="Claim your rewards!")
    async def claim(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.send_message("Please wait...", ephemeral=True)
        cur.execute("SELECT level FROM user_stats WHERE user_id = %s", (str(interaction.user.id),))
        if not cur.fetchone():
            await interaction.edit_original_response("You have not opened a room yet! Type /create_room then try this command again!")
            return
        for item in config.items:
            if item[3] <= cur.fetchone()[0]:
                cur.execute(f"UPDATE member_inventory SET {item[4]} = 1 WHERE user_id = %s", (str(interaction.response.id),))
                db.commit()
                await interaction.edit_original_response(f"Congrats, you have claimed the **{item[0]}**!")
                return
        await interaction.edit_original_response("You have nothing to claim!")
def setup(bot: commands.Bot):
    bot.add_cog(Rewards(bot))