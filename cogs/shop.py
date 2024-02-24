import disnake
from disnake.ext import commands
import config

db = config.db

cur = config.cur

class Shop(commands.Bot):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="shop", description="Buy or sell your stuff!")
    async def shop(interaction: disnake.Interaction):
        await interaction.response.send_message("Please wait...", ephemeral=True)
        cur.execute("SELECT * FROM user_stats WHERE user_id = %s", (str(interaction.user.id),))
        if not cur.fetchone():
            await interaction.edit_original_response("Whoops! Seems like you have not created a room yet! Create it first then try to use this command again.")
            return
        items = [
            ["🥶 Air conditioner", "Here, have some cold air during a hot summer day! (Multiplies XP by 1.5x)", 1.5, 3],
            ["👗 Clothes valet", "A place to keep your favorite dress in! (Multiplies XP by 2x)", 2, 5],
            ["🛏️ Bed", "A place for you to rest after a long day! (Multiplies XP by 3x)", 2, 7],
            ["🏮 Desk lamp", "Here, some light for you to do your homework, requires a desk. (multiplies XP by 9x)", 2, 9],
            ["🍼 Crib", "Here, A place for your baby to sleep! (multiplies XP by 9x)", 3, 11],
            ["🪑 Beside table", "You can put the late night books that you read on this!", 5, 13],
            ["📗 Book shelf", "You can put all your novels inside of this!", 7, 15],
            ["🗄️ Desk", "Something you can do your homework on!", 9.9, 17]
        ]
        embed = disnake.Embed(title="Welcome to the shop!", description=f"Buy whatever you want, {interaction.user.mention}!")
        for i in items:
            embed.add_field(name=i[0], value=i[1], inline=False)
        await interaction.edit_original_response(embed=embed, content="")
        return

def setup(bot: commands.Bot):
  bot.add_cog(Shop(bot))