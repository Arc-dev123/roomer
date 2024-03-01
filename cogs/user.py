import disnake
from disnake.ext import commands
import config

db = config.db

cur = config.cur

class User(commands.Cog):

  def __init__(self, bot: commands.Bot):
    self.bot = bot
  
  @commands.slash_command(name="set_room", description="Lets the user create a room")
  async def set_room(interaction: disnake.CommandInteraction, channel: disnake.TextChannel):
    await interaction.response.send_message("Please wait...", ephemeral=True)
    cur.execute("SELECT * FROM server WHERE server_id = %s", (str(interaction.guild_id),))
    if not cur.fetchone():
        await interaction.edit_original_response(
            "Whoops! It seems like the server didn't setup the bot yet... tell an administrator to set it up!")
        return
    cur.execute("SELECT * FROM member WHERE user_id = %s AND server_id = %s", (str(interaction.user.id), str(interaction.guild.id)))
    if cur.fetchone():
        cur.execute("UPDATE member SET channel_id = %s WHERE user_id = %s AND server_id = %s", (channel.id, str(interaction.user.id), str(interaction.guild.id),))
    elif not cur.fetchone():
        cur.execute("INSERT INTO member VALUES (%s, %s, %s)", (str(interaction.user.id), str(interaction.guild.id), channel.id,))
    db.commit()
    await interaction.edit_original_response(f"Your channel has been set! <#{channel.id}>")

  @commands.slash_command(name="stats", description="Lets the user see their stats")
  async def stats(interaction: disnake.CommandInteraction):
    cur.execute("SELECT * FROM server WHERE server_id = %s", (str(interaction.guild_id),))
    if not cur.fetchone():
        await interaction.edit_original_response("Whoops! It seems like the server didn't setup the bot yet... tell an administrator to set it up!")
        return
    cur.execute("SELECT xp, level FROM user_stats WHERE user_id = %s", (str(interaction.user.id),))
    info = cur.fetchone()
    if info == None:
      await interaction.response.send_message("You don't have any stats yet! Create a room first!", ephemeral=True)
      return
    embed = disnake.Embed(title=f"{interaction.author.name}'s **STATS:**", description=f"**XP:** {info[0]}/{25 * info[1]}\n\n**Level:** {info[1]}", color=disnake.Color.green())
    await interaction.response.send_message(embed=embed)

  @commands.slash_command(name="add_user", description="Lets the user to add more members into their group")
  async def add_user(interaction: disnake.CommandInteraction, user: str):
    await interaction.response.send_message("Please wait...", ephemeral=True)
    cur.execute("SELECT room_key FROM server WHERE server_id = %s", (str(interaction.guild_id),))
    if not cur.fetchone():
        await interaction.edit_original_response(
            "Whoops! It seems like the server didn't setup the bot yet... tell an administrator to set it up!")
        return
    cur.execute("SELECT channel_id FROM member WHERE server_id = %s and user_id = %s", (str(interaction.guild_id), str(interaction.user.id),))
    channel_id = cur.fetchone()[0]
    channel = disnake.utils.get(interaction.guild.channels, id=channel_id)
    if channel_id:
      user = interaction.guild.get_member(int(user))
      if not user:
        await interaction.edit_original_response("Whoops! It seems like the user you mentioned does not exist!")
        return
      await channel.set_permissions(user,
                    read_message_history=True,
                    read_messages=True,
                    send_messages=True
      )
      await interaction.edit_original_response(f"Done, {user.mention} can now chat in <#{channel_id}>")
      await user.send(f"You can now chat in <#{channel_id}>!")
      return
    await interaction.edit_original_response("You haven't made a room yet! Create a room first!")

  @commands.slash_command(name="remove_user", description="Lets the user to remove members from their group")
  async def remove_user(interaction: disnake.CommandInteraction, user: str):
    await interaction.response.send_message("Please wait...", ephemeral=True)
    cur.execute("SELECT room_key FROM server WHERE server_id = %s", (str(interaction.guild_id),))
    if not cur.fetchone():
        await interaction.edit_original_response("Whoops! It seems like the server didn't setup the bot yet... tell an administrator to set it up!")
        return
    cur.execute("SELECT channel_id FROM member WHERE server_id = %s and user_id = %s", (str(interaction.guild_id), str(interaction.user.id),))
    channel_id = cur.fetchone()[0]
    channel = disnake.utils.get(interaction.guild.channels, id=channel_id)
    if channel_id:
      user = interaction.guild.get_member(int(user))
      await channel.set_permissions(user,
                    read_message_history=False,
                    read_messages=False,
                    send_messages=False
      )
      await interaction.edit_original_response(f"Done, {user.mention} has been removed from chatting in <#{channel_id}>")
      await user.send(f"You have been removed from <#{channel_id}>!")
      return
    await interaction.edit_original_response("You haven't made a room yet! Create a room first!")

  @commands.slash_command(name="purge", description="Deletes all messages from the user's room")
  async def purge(interaction: disnake.CommandInteraction):
      await interaction.response.send_message("Please wait...", ephemeral=True)
      cur.execute("SELECT room_key FROM server WHERE server_id = %s", (str(interaction.guild_id),))
      if not cur.fetchone():
          await interaction.edit_original_response(
              "Whoops! It seems like the server didn't setup the bot yet... tell an administrator to set it up!")
          return
      cur.execute("SELECT channel_id FROM member WHERE user_id = %s AND server_id = %s", (str(interaction.user.id), str(interaction.guild.id),))
      channel_id = cur.fetchone()[0]
      if not channel_id:
          await interaction.edit_original_response(
              "Whoops! Seems like you don't have a room in this server. Use /create_room to create a room first!")
          return
      channel = disnake.utils.get(interaction.guild.text_channels, id=channel_id)
      async for message in channel.history(limit=None):
          await message.delete()
      return

def setup(bot: commands.Bot):
  bot.add_cog(User(bot))