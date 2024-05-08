import psycopg2

secret = "" #Insert your bot token

cogs = ["cogs.admin", "cogs.user", "cogs.item"]

items = [
            [
              "🥶 A/C",
              "It's really chilly, maybe keep the temperature down!", 2, 5, "ac"],
            [
              "👗 Clothes Valet",
              "Maybe keep your favorite dress up here to make all your friends jealous!", 4, 10, "clothes_valet"],
            [
              "🛏️ Bed",
              "A place for you to rest after a long day of work!", 6, 15, "bed"],
            [
              "💡 Desk Lamp",
              "A bright light is always right!", 12, 20, "desk_lamp"],
            [
              "👶 Crib", "A place where you can put your baby in.", 16, 25, "crib"],
            [
              "📗 Beside Table", "A place to put your late night books!", 20, 30, "b_table"],
            [
              "📚 Book Shelf", "Here, put all your romance novel inside of it!", 24, 35, "book_shelf"],
            [
              "🗄️ Desk", "A desk to put your desktop in!", 30, 40, "desk"],
            [
              "🕛 Clock", "Maybe try to keep the time in your hands.", 34, 45, "clock"],
            [
              "🪞 Mirror", "Look at that attractive face, my guy!", 38, 50, "mirror"],
            [
              "🖼️ Painting", "Keep your most memorable memories in that!", 100, 100, "painting"]
        ]


db = psycopg2.connect(
  dbname="",
  user="",
  password="",
  host=""
)

#Insert all info as needed

cur = db.cursor()


db.commit()
