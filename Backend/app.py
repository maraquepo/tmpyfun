import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify

SELECT_5 = (
  'SELECT id, fullname, passwordhash, institution, bio, creator_user_id, public_user_id, picture, email, "signupIP", "createdAt", "updatedAt", "tokenBalance" FROM "Users" ORDER BY "createdAt" LIMIT 5'
)

SELECT_ALL_OLDEST_FIRST = (
  'SELECT id, fullname, passwordhash, institution, bio, creator_user_id, public_user_id, picture, email, "signupIP", "createdAt", "updatedAt", "tokenBalance" FROM "Users" ORDER BY "createdAt" '
)

load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

def transform_user_data(data):
    keys = [
        "id", "fullname", "passwordhash", "institution", "bio",
        "creator_user_id", "public_user_id", "picture", "email",
        "signupIP", "createdAt", "updatedAt", "tokenBalance"
    ]
    return [dict(zip(keys, row)) for row in data]

@app.get("/api/users")
def get_all_users():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_OLDEST_FIRST)
            data = cursor.fetchall()
    transformed_data = transform_user_data(data)
    return jsonify(transformed_data)

@app.get("/api/oldusers")
def get_old_users():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_5)
            data = cursor.fetchall()
    transformed_data = transform_user_data(data)
    return jsonify(transformed_data)

if __name__ == "__main__":
    app.run(debug=False)