import disnake
from disnake.ext import commands
import sqlite3
import config

intent = disnake.Intents.all()
bot = commands.Bot(intents=intent, command_prefix="~")
db = sqlite3.connect("main.db")
cur = db.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS server (
                    server_id TEXT,
                    room_category INT,
                    room_key INT
                )"""
            )

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

bot.remove_command('help')


@bot.event
async def on_ready():
    print("Ready for service!")

@bot.event
async def on_message(message):
  try:
    cur.execute("SELECT user_id FROM user WHERE user_id = ?", (str(message.author.id),))
    if cur.fetchone() is not None:
      cur.execute("SELECT xp, level FROM user_stats WHERE user_id = ?", (str(message.author.id),))
      info = cur.fetchall()
      if info[0] >= info[1] * 500:
        cur.execute("UPDATE user_stats SET xp = ?, level = ? WHERE user_id = ?", (0, info[1] + 1, str(message.author.id),))
        db.commit()
        await message.channel.send(f"Congratulations, {message.author.mention}! You've reached level {info[1] + 1}!", ephemeral=True)
  except Exception as e:
    print(e)
  try:
    channel = message.channel
    cur.execute("SELECT user_id FROM user WHERE channel_id = ?", (channel.id,))
    info = cur.fetchone()

    if info:
      user_id = info[0]
      print("User ID:", user_id)

      cur.execute("UPDATE user_stats SET xp = xp + 1 WHERE user_id = ?", (user_id,))
      db.commit()

      cur.execute("SELECT xp FROM user_stats WHERE user_id = ?", (user_id,))
      xp = cur.fetchone()[0]
      print("Updated XP:", xp)

    else:
      print("Channel not found in database")
  except Exception as e:
    print("An error occurred:", e)
for cog in config.cogs:
  bot.load_extension(cog)

bot.run(config.secret)
