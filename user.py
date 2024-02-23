import disnake
from disnake.ext import commands
import sqlite3

db = sqlite3.connect("main.db")
cur = db.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS user (
                    user_id TEXT,
                    server_id TEXT,
                    channel_id INT
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS user_stats (
                    user_id TEXT,
                    xp INT,
                    level INT
)""")
db.commit()

class User(commands.Cog):

  def __init__(self, bot: commands.Bot):
    self.bot = bot
  
  @commands.slash_command(name="create_room")
  async def create_room(interaction: disnake.CommandInteraction, name: str):
      cur.execute("SELECT room_key FROM server WHERE server_id = ?", (str(interaction.guild_id),))
      role = cur.fetchone()[0]
      role = disnake.utils.get(interaction.guild.roles, id=role)
      if not role in interaction.user.roles:
        await interaction.response.send_message("Whoops! It seems like you do not have the room key! Ask your server admin to give you the key first!", ephemeral=True)
        return
      cur.execute("SELECT room_category FROM server WHERE server_id = ?", (str(interaction.guild_id),))
      r_cate = cur.fetchone()[0]
      r_cate = disnake.utils.get(interaction.guild.categories, id=r_cate)
      channel = await interaction.guild.create_text_channel(name=name, category=r_cate)

      cur.execute("INSERT INTO user VALUES (?, ?, ?)", (str(interaction.user.id), str(interaction.guild_id), channel.id,))
      cur.execute("INSERT INTO user_stats VALUES (?, ?, ?)", (str(interaction.user.id), 0, 1,))
      db.commit()
      await channel.set_permissions(interaction.guild.default_role,
                    read_message_history=False,
                    read_messages=False
      )
      await channel.set_permissions(interaction.author,
                    read_message_history=True,
                    read_messages=True,
                    send_messages=True
      )
      await channel.send(f"Welcome to your room, {interaction.user.mention}!")
      await interaction.response.send_message(f"Done, check out your room in <#{channel.id}>!", ephemeral=True)
      return
  
  @commands.slash_command(name="delete_room")
  async def delete_room(interaction: disnake.CommandInteraction):
    cur.execute("SELECT room_key FROM server WHERE server_id = ?", (str(interaction.guild_id),))
    role = cur.fetchone()[0]
    role = disnake.utils.get(interaction.guild.roles, id=role)
    if not role in interaction.user.roles:
      await interaction.response.send_message("Whoops! It seems like you do not have the room key! Ask your server admin to give you the key first!", ephemeral=True)
      return

    cur.execute("SELECT channel_id FROM user WHERE user_id = ? AND server_id = ?", (str(interaction.user.id), str(interaction.guild_id),))

    channel_id = cur.fetchone()[0]
    channel = disnake.utils.get(interaction.guild.channels, id=channel_id)
    await channel.delete()
    cur.execute("DELETE FROM user WHERE user_id = ? AND server_id = ?", (str(interaction.user.id), str(interaction.guild_id),))
    cur.execute("DELETE FROM user_stats WHERE user_id = ?", (str(interaction.user.id), str(interaction.guild_id),))
    db.commit()
    if interaction.channel_id == channel_id:
      await interaction.user.send("Done, your room has been deleted!")
      return
    await interaction.response.send_message("Done, your room has been deleted!", ephemeral=True)
    return
    
  @commands.slash_command(name="stats")
  async def stats(interaction: disnake.CommandInteraction):
    cur.execute("SELECT xp, level FROM user_stats WHERE user_id = ?", (str(interaction.user.id),))
    info = cur.fetchone()
    if info == None:
      await interaction.response.send_message("You don't have any stats yet! Create a room first!", ephemeral=True)
      return
    embed = disnake.Embed(title=f"{interaction.author.name}'s **STATS:**", description=f"**XP:** {info[0]}\n**Level:** {info[1]}", color=disnake.Color.green())
    await interaction.response.send_message(embed=embed)

  @commands.slash_command(name="add_user")
  async def add_user(interaction: disnake.CommandInteraction, user: str):
    cur.execute("SELECT channel_id FROM user WHERE server_id = ? and user_id = ?", (str(interaction.guild_id), str(interaction.user.id),))
    channel_id = cur.fetchone()[0]
    channel = disnake.utils.get(interaction.guild.channels, id=channel_id)
    if channel_id:
      user = interaction.guild.get_member(int(user))
      if not user:
        await interaction.response.send_message("Whoops! It seems like the user you mentioned does not exist!", ephemeral=True)
        return
      await channel.set_permissions(user,
                    read_message_history=True,
                    read_messages=True,
                    send_messages=True
      )
      await interaction.response.send_message(f"Done, {user.mention} can now chat in <#{channel_id}>", ephemeral=True)
      await user.send(f"You can now chat in <#{channel_id}>!")
      return
    await interaction.response.send_message("You haven't made a room yet! Create a room first!", ephemeral=True)

  @commands.slash_command(name="remove_user")
  async def remove_user(interaction: disnake.CommandInteraction, user: str):
    cur.execute("SELECT channel_id FROM user WHERE server_id = ? and user_id = ?", (str(interaction.guild_id), str(interaction.user.id),))
    channel_id = cur.fetchone()[0]
    channel = disnake.utils.get(interaction.guild.channels, id=channel_id)
    if channel_id:
      user = interaction.guild.get_member(int(user))
      await channel.set_permissions(user,
                    read_message_history=False,
                    read_messages=False,
                    send_messages=False
      )
      await interaction.response.send_message(f"Done, {user.mention} has been removed from chatting in <#{channel_id}>", ephemeral=True)
      await user.send(f"You have been removed from <#{channel_id}>!")
      return
    await interaction.response.send_message("You haven't made a room yet! Create a room first!", ephemeral=True)
    
def setup(bot: commands.Bot):
  bot.add_cog(User(bot)) 