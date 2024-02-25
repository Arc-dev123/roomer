import disnake
from disnake.ext import commands
import config

db = config.db
cur = config.cur

class Rewards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="rewards", description="Check out the rewards!")
    async def shop(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.send_message("Please wait...", ephemeral=True)
        cur.execute("SELECT * FROM user_stats WHERE user_id = %s", (str(interaction.user.id),))
        if not cur.fetchone():
            await interaction.response.send_message("Whoops! Seems like you have not created a room yet! Create it first then try to use this command again.")
            return
        items = [
            ["🥶 A/C", "It's really chilly, maybe keep the temperature down!", 1.5, 5],
            ["👗 Clothes Valet", "Maybe keep your favorite dress up here to make all your friends jealous!", 3, 10],
            ["🛏️ Bed", "A place for you to rest after a long day of work!", 6, 15],
            ["💡 Desk Lamp", "A bright light is always right!", 12, 20],
            ["👶 Crib", "A place where you can put your baby in.", 16, 25],
            ["📗 Beside Table", "A place to put your late night books!", 20, 30],
            ["📚 Book Shelf", "Here, put all your romance novel inside of it!", 24, 35],
            ["🗄️ Desk", "A desk to put your desktop in!", 30, 40],
            ["🕛 Clock", "Maybe try to keep the time in your hands.", 34, 45],
            ["🪞 Mirror", "Look at that attractive face, my guy!", 38, 50],
            ["🖼️ Painting", "Keep your most memorable memories in that!", 100, 100]
        ]
        embed = disnake.Embed(title="Rewards...")
        for item in items:
            embed.add_field(name=f"{item[0]} (Requires level {item[3]})", value=f"{item[1]} **(Multiplies xp by {item[2]}x)**\n", inline=False)
        await interaction.edit_original_response(embed=embed, content="")
        return

def setup(bot: commands.Bot):
    bot.add_cog(Rewards(bot))