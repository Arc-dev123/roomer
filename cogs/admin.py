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
  async def set_bot(interaction: disnake.CommandInteraction):
    await interaction.response.send_message("Please wait...", ephemeral=True)
    category = await interaction.guild.create_category("ROOMER")
    role = await interaction.guild.create_role(name="Roomer key")
    cur.execute("SELECT * FROM server WHERE server_id = %s", (str(interaction.user.id),))
    if not cur.fetchone():
      cur.execute("UPDATE server SET room_category = %s WHERE user_id = %s", (category.id,))
      cur.execute("UPDATE server SET room_key = %s WHERE user_id %s", (role.id,))
      db.commit()
    elif cur.fetchone():
      cur.execute("INSERT INTO server VALUES (%s, %s, %s)", (str(interaction.guild_id), category.id, role.id,))
      db.commit()
    embed = disnake.Embed(
        title="You're good to go!",
        description="Thank you for setting up!\n* To create a new room just type /create_room (the user must have the room key role)",
        color=disnake.Color.green()
    )
    await interaction.edit_original_response(content="", embed=embed)
    return

  

def setup(bot: commands.Bot):
  bot.add_cog(Admin(bot))
