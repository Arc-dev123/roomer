import psycopg2

secret = "MTIwOTEzMjgxMzAyMzE5MTA2MA.GPwxHf.64eJMSHgauM7ZT9kk9wnAzLlMZWWb487ec3Twg"

cogs = ["cogs.admin", "cogs.user", "cogs.item"]

items = [
            ["🥶 A/C", "It's really chilly, maybe keep the temperature down!", 1.5, 5, "AC"],
            ["👗 Clothes Valet", "Maybe keep your favorite dress up here to make all your friends jealous!", 3, 10, "clothes_valet"],
            ["🛏️ Bed", "A place for you to rest after a long day of work!", 6, 15, "bed"],
            ["💡 Desk Lamp", "A bright light is always right!", 12, 20, "desk_lamp"],
            ["👶 Crib", "A place where you can put your baby in.", 16, 25, "crib"],
            ["📗 Beside Table", "A place to put your late night books!", 20, 30, "b_table"],
            ["📚 Book Shelf", "Here, put all your romance novel inside of it!", 24, 35, "book_shelf"],
            ["🗄️ Desk", "A desk to put your desktop in!", 30, 40, "desk"],
            ["🕛 Clock", "Maybe try to keep the time in your hands.", 34, 45, "clock"],
            ["🪞 Mirror", "Look at that attractive face, my guy!", 38, 50, "mirror"],
            ["🖼️ Painting", "Keep your most memorable memories in that!", 100, 100, "painting"]
        ]

db = psycopg2.connect(
  dbname="postgres",
  user="postgres.xclltlpuejthyjjsdsyv",
  password="ROBUXGUD123",
  host="aws-0-ap-south-1.pooler.supabase.com",
  port=5432
)

cur = db.cursor()


