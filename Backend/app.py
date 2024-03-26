import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.String(), primary_key=True)
    fullname = db.Column(db.String())
    passwordhash = db.Column(db.String())
    institution = db.Column(db.String())
    bio = db.Column(db.String())
    creator_user_id = db.Column(db.String())
    public_user_id = db.Column(db.String())
    picture = db.Column(db.String())
    email = db.Column(db.String())
    signupIP = db.Column(db.String())
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    tokenBalance = db.Column(db.Integer)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@app.route("/api/users")
def get_all_users():
    users = User.query.order_by(desc(User.createdAt)).all()
    return jsonify([user.as_dict() for user in users])

@app.route("/api/oldusers")
def get_old_users():
    users = User.query.order_by(User.createdAt).limit(5).all()
    return jsonify([user.as_dict() for user in users])

@app.route("/api/change_picture/<string:id>", methods=["PATCH"])
def change_picture(id):
  data = request.get_json()
  new_picture = data.get('picture')

  user = User.query.get(id)

  if user:
    user.picture = new_picture
    db.session.commit()
    return jsonify({'message': 'Picture updated sucessfully'})
  else:
    return jsonify({'error': 'User not found'}), 404

if __name__ == "__main__":
    app.run(debug=False)
