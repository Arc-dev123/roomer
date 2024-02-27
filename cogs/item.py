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
        cur.execute("SELECT room_key FROM server WHERE server_id = %s", (str(interaction.guild_id),))
        if not cur.fetchone():
            await interaction.edit_original_response(
                "Whoops! It seems like the server didn't setup the bot yet... tell an administrator to set it up!")
            return
        cur.execute("SELECT * FROM user_stats WHERE user_id = %s", (str(interaction.user.id),))
        if not cur.fetchone():
            await interaction.response.send_message("Whoops! Seems like you have not created a room yet! Create it first then try to use this command again.")
            return

        embed = disnake.Embed(title="Rewards...")
        for item in config.items:
            cur.execute(f"SELECT {item[4]} FROM member_inventory WHERE user_id = %s", (str(interaction.user.id),))
            if cur.fetchone()[0] == 0:
                embed.add_field(name=f"{item[0]} (Requires level {item[3]})", value=f"{item[1]} **(Multiplies xp by {item[2]}x)**", inline=False)
            else:
                cur.execute(f"SELECT {item[4]} FROM member_inventory WHERE user_id = %s", (str(interaction.user.id),))
                embed.add_field(name=f"{item[0]} ✅", value=f"{item[1]} **(Multiplies xp by {item[2]}x)**", inline=False)
        await interaction.edit_original_response(embed=embed, content="")
        return

    @commands.slash_command(name="claim", description="Claim your rewards!")
    async def claim(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.send_message("Please wait...", ephemeral=True)
        cur.execute("SELECT room_key FROM server WHERE server_id = %s", (str(interaction.guild_id),))
        if not cur.fetchone():
            await interaction.edit_original_response(
                "Whoops! It seems like the server didn't setup the bot yet... tell an administrator to set it up!")
            return
        cur.execute("SELECT level FROM user_stats WHERE user_id = %s", (str(interaction.user.id),))
        level = cur.fetchone()[0]
        x = ""
        for item in config.items:
            cur.execute(f"SELECT {item[4]} FROM member_inventory WHERE user_id = %s", (str(interaction.user.id),))
            if item[3] <= level:
                if cur.fetchone()[0] == 0:
                    cur.execute(f"UPDATE member_inventory SET {item[4]} = 1 WHERE user_id = %s", (str(interaction.user.id),))
                    db.commit()
                    x += f"Now you have **{item[0]}**!\n"
        if x == "":
            await interaction.edit_original_response("There is nothing to claim!")
            return
        await interaction.edit_original_response(x)
        return
def setup(bot: commands.Bot):
    bot.add_cog(Rewards(bot))