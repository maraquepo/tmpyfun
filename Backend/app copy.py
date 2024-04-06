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

class Team(db.Model):
    __tablename__ = 'Teams'

    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String())
    type = db.Column(db.String())
    public_team_id = db.Column(db.String())
    picture = db.Column(db.String())
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)
    creatorId = db.Column(db.String(), db.ForeignKey('Users.id'))

    creator = db.relationship('User', backref='teams')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# Caching mechanism
user_cache = {}
team_cache = {}

def fetch_users():
    if not user_cache:
        users = User.query.order_by(desc(User.createdAt)).all()
        user_cache['all'] = [user.as_dict() for user in users]
    return user_cache['all']


# Routes
@app.route("/api/users")
def get_all_users():
    users = User.query.order_by(desc(User.createdAt)).all()
    return jsonify([user.as_dict() for user in users])

@app.route("/api/oldusers")
def get_old_users():
    users = User.query.order_by(User.createdAt).limit(5).all()
    return jsonify([user.as_dict() for user in users])

@app.route("/api/user/<string:id>", methods=["PUT"])
def edit_user(id):
    data = request.json

    user = User.query.filter_by(id=id).first()
    print("user",user)
    print("data", data)

    if user:
        # Update user attributes based on the provided data
        for key, value in data.items():
            setattr(user, key, value)

        db.session.commit()
        return jsonify({'message': 'User Updated'})
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route("/api/team/<string:id>", methods=["PUT"])
def edit_team(id):
    data = request.json

    team = Team.query.filter_by(id=id).first()

    print("team", team)
    print("data", data)
    if team:
        # Update team attributes based on the provided data
        for key, value in data.items():
            setattr(team, key, value)

        db.session.commit()
        return jsonify({'message': 'Team Updated'})
    else:
        return jsonify({'error': 'Team not found'}), 404

@app.route("/api/users/delete", methods=["DELETE"])
def delete_multiple_users():
    data = request.json
    user_ids = data.get("userIDs", [])

    if not user_ids:
        return jsonify({'error': 'No user IDs provided'}), 400

    try:
        deleted_count = User.query.filter(User.id.in_(user_ids)).delete()
        db.session.commit()

        return jsonify({'message': f'{deleted_count} users deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route("/api/users/update-picture-url", methods=["PUT"])
def update_multiple_users_picture_url():
    data = request.json
    user_ids = data.get("userIDs", [])
    new_picture_url = data.get("newPictureURL", "")

    if not user_ids:
        return jsonify({'error': 'No user IDs provided'}), 400

    if not new_picture_url:
        return jsonify({'error': 'New picture URL cannot be empty'}), 400

    try:
        updated_count = User.query.filter(User.id.in_(user_ids)).update({User.picture: new_picture_url}, synchronize_session=False)
        db.session.commit()

        return jsonify({'message': f'Updated {updated_count} user picture URLs'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route("/api/teams/update-picture-url", methods=["PUT"])
def update_multiple_teams_picture_url():
    data = request.json
    team_ids = data.get("teamIDs", [])
    new_picture_url = data.get("newPictureURL", "")

    if not team_ids:
        return jsonify({'error': 'No team IDs provided'}), 400

    if not new_picture_url:
        return jsonify({'error': 'New picture URL cannot be empty'}), 400

    try:
        updated_count = Team.query.filter(Team.id.in_(team_ids)).update({Team.picture: new_picture_url}, synchronize_session=False)
        db.session.commit()

        return jsonify({'message': f'Updated {updated_count} user picture URLs'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route("/api/teams")
def get_all_teams():
    teams = db.session.query(
        Team.id,
        Team.title,
        Team.type,
        Team.picture,
        Team.createdAt,
        Team.updatedAt,
        Team.creatorId,
        Team.public_team_id,
        User.fullname
    ).join(User).filter(
        Team.creatorId.isnot(None)
    ).order_by(Team.createdAt).all()

    return jsonify([dict(zip(['id','title', 'type', 'picture', 'createdAt', 'updatedAt', 'creatorId', 'public_team_id','creator_fullname'], team)) for team in teams])

if __name__ == "__main__":
    app.run(debug=False)
