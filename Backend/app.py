import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify

SELECT_5 = (
  'SELECT * FROM "Users" ORDER BY "createdAt" LIMIT 5'
)

SELECT_ALL_OLDEST_FIRST = (
  'SELECT * FROM "Users" ORDER BY "createdAt" '
)

load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@app.get("/api/users")
def get_all_users():
  with connection:
    with connection.cursor() as cursor:
      cursor.execute(SELECT_ALL_OLDEST_FIRST)
      data = cursor.fetchall()
  return jsonify(data)

@app.get("/api/oldusers")
def get_old_users():
  with connection:
    with connection.cursor() as cursor:
      cursor.execute(SELECT_5)
      data = cursor.fetchall()
  return jsonify(data)

if __name__ == "__main__":
  app.run(debug=False)
