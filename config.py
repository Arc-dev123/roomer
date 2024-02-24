import psycopg2

cogs = ["cogs.admin", "cogs.user"]

secret = "MTIwOTEzMjgxMzAyMzE5MTA2MA.GPwxHf.64eJMSHgauM7ZT9kk9wnAzLlMZWWb487ec3Twg"

db = psycopg2.connect(
  dbname="postgres",
  user="postgres.xclltlpuejthyjjsdsyv",
  password="ROBUXGUD123",
  host="aws-0-ap-south-1.pooler.supabase.com",
  port=5432
)

cur = db.cursor()


