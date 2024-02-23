import disnake
from disnake.ext import commands
import sqlite3

db = sqlite3.connect("main.db")
cur = db.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS server (
                    server_id TEXT,
                    room_category INT,
                    room_key INT
                )"""
            )
db.commit()

class Admin(commands.Cog):

  def __init__(self, bot: commands.Bot):
    self.bot = bot
  
  @commands.slash_command(name="setup")
  @commands.has_permissions(administrator=True)
  async def set_bot(interaction: disnake.CommandInteraction):
      category = await interaction.guild.create_category("ROOMER")
      role = await interaction.guild.create_role(name="Roomer key")
      cur.execute("INSERT INTO server VALUES (?, ?, ?)", (str(interaction.guild_id), category.id, role.id,))
      db.commit()
      embed = disnake.Embed(
          title="You're good to go!",
          description="Thank you for setting up!\n* To create a new room just type /create_room (the user must have the room key role)",
          color=disnake.Color.green()
      )
      await interaction.response.send_message(embed=embed, ephemeral=True)
      return
  

def setup(bot: commands.Bot):
  bot.add_cog(Admin(bot))