import disnake
from disnake.ext import commands
import sqlite3
import config

intent = disnake.Intents.all()
bot = commands.Bot(intents=intent, command_prefix="~")

db = config.db

cur = config.cur

db.commit()

bot.remove_command('help')

@bot.event
async def on_ready():
    print("Ready for service!")

@bot.event
async def on_message(message):
  try:
    cur.execute("SELECT user_id FROM member WHERE user_id = %s", (str(message.author.id),))
    if cur.fetchone() is not None:
      cur.execute("SELECT xp, level FROM user_stats WHERE user_id = %s", (str(message.author.id),))
      info = cur.fetchall()
      if info[0][0] >= info[0][1] * 25:
        cur.execute("UPDATE user_stats SET xp = 0, level = level + 1 WHERE user_id = %s", (str(message.author.id),))
        db.commit()
  except Exception as e:
    print(e)
  try:
    channel = message.channel
    cur.execute("SELECT user_id FROM member WHERE channel_id = %s", (channel.id,))
    info = cur.fetchone()

    if info:
      user_id = info[0]

      cur.execute("UPDATE user_stats SET xp = xp + 1 WHERE user_id = %s", (user_id,))
      db.commit()

      cur.execute("SELECT xp FROM user_stats WHERE user_id = %s", (user_id,))

    else:
      print("Channel not found in database")
  except Exception as e:
    print("An error occurred:", e)
  return
for cog in config.cogs:
  bot.load_extension(cog)

bot.run(config.secret)
