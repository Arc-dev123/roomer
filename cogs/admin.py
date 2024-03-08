import disnake
from disnake.ext import commands
import config

db = config.db

cur = config.cur

class Admin(commands.Cog):

  def __init__(self, bot: commands.Bot):
    self.bot = bot
  
  @commands.slash_command(name="setup", description="Sets up the bot to be used in your server.")
  @commands.has_permissions(administrator=True)
  async def set_bot(interaction: disnake.ApplicationCommandInteraction, category: disnake.CategoryChannel, role: disnake.Role):
    try:
      await interaction.response.send_message("Please wait...", ephemeral=True)
      cur.execute("SELECT * FROM server WHERE server_id = %s", (str(interaction.guild.id),))
      if cur.fetchone():
        cur.execute("UPDATE server SET room_category = %s WHERE user_id = %s", (category.id, str(interaction.user.id),))
        cur.execute("UPDATE server SET room_key = %s WHERE user_id = %s", (role.id, str(interaction.user.id),))
        db.commit()
      if not cur.fetchone():
        cur.execute("INSERT INTO server VALUES (%s, %s, %s)", (str(interaction.guild.id), category.id, role.id,))
        db.commit()
      await interaction.edit_original_response(f"Your server has been set successfully! Users can now create rooms using /create_room!")
      return
    except Exception as e:
      await interaction.response.send_message("An error occurred: ", e)

def setup(bot: commands.Bot):
  bot.add_cog(Admin(bot))
