import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, func
from cachetools import TTLCache
from sqlalchemy.sql import extract
from datetime import datetime, timedelta
from sqlalchemy import case

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# TTL Cache configuration
user_cache = TTLCache(maxsize=1000, ttl=1)
team_cache = TTLCache(maxsize=1000, ttl=300)
coupon_cache = TTLCache(maxsize=1000, ttl=300)

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
    verifiedDT = db.Column(db.DateTime)
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

class Coupon(db.Model):
    __tablename__ = 'Coupons'

    promo_code = db.Column(db.String, primary_key=True)
    number_of_tokens = db.Column(db.Integer)
    expiration_date = db.Column(db.DateTime)
    creation_date = db.Column(db.DateTime)
    description = db.Column(db.String)
    clicked_count = db.Column(db.Integer)
    max_users = db.Column(db.Integer)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

def fetch_users():
    cached_users = user_cache.get("all_users")
    if cached_users:
        return cached_users

    users = User.query.order_by(desc(User.createdAt)).all()
    serialized_users = [user.as_dict() for user in users]
    user_cache["all_users"] = serialized_users
    return serialized_users

def fetch_teams():
    cached_teams = team_cache.get("all_teams")
    if cached_teams:
        return cached_teams

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
    ).order_by(desc(Team.createdAt)).all()

    serialized_teams = [dict(zip(['id','title', 'type', 'picture', 'createdAt', 'updatedAt', 'creatorId', 'public_team_id','creator_fullname'], team)) for team in teams]
    team_cache["all_teams"] = serialized_teams
    return serialized_teams

def fetch_coupons():
    cached_coupons = coupon_cache.get("all_coupons")
    if cached_coupons:
        return cached_coupons

    coupons = Coupon.query.all()
    serialized_coupons = [coupon.as_dict() for coupon in coupons]
    coupon_cache["all_coupons"] = serialized_coupons
    return serialized_coupons

# Routes

@app.route("/api/users")
def get_all_users():
    users = fetch_users()
    return jsonify(users)

@app.route("/api/teams")
def get_all_teams():
    teams = fetch_teams()
    return jsonify(teams)

@app.route("/api/coupons")
def get_all_coupons():
    coupons = fetch_coupons()
    return jsonify(coupons)

@app.route("/api/oldusers")
def get_old_users():
    users = fetch_users()[:5]  # Get the first 5 users
    return jsonify(users)

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
        # Invalidate team cache
        team_cache.clear()
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

@app.route("/api/users/update-created-at", methods=["PUT"])
def update_multiple_users_created_at():
    data = request.json
    user_ids = data.get("userIDs", [])

    if not user_ids:
        return jsonify({'error': 'No user IDs provided'}), 400

    try:
        # Fetch users by IDs
        users = User.query.filter(User.id.in_(user_ids)).all()

        # Update the createdAt attribute of each user
        for user in users:
            # Subtract one year from the current createdAt value
            new_created_at = user.createdAt - timedelta(days=492)
            new_updated_at = user.updatedAt - timedelta(days=492)

            user.createdAt = new_created_at
            user.updatedAt = new_updated_at

        db.session.commit()

        return jsonify({'message': f'Updated createdAt attribute for {len(users)} users'})
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

@app.route("/api/accounts/creation-stats")
def get_account_creation_stats():
    # Query to fetch the month_year, count of created accounts,
    # count of verified accounts, and count of unverified accounts
    creation_stats = db.session.query(
        func.date_trunc('month', User.createdAt).label('month_year'),
        func.count().label('total_accounts_created'),
        func.sum(case((User.verifiedDT != None, 1), else_=0)).label('verified_accounts'),
        func.sum(case((User.verifiedDT == None, 1), else_=0)).label('unverified_accounts')
    ).group_by('month_year').order_by('month_year').all()

    # Serialize the results
    serialized_stats = [
        {
            'month_year': stat[0],
            'total_accounts_created': stat[1],
            'verified_accounts': stat[2],
            'unverified_accounts': stat[3]
        }
        for stat in creation_stats
    ]

    return jsonify(serialized_stats)

# @app.route("/api/accounts/creation-stats")
# def get_account_creation_stats():
#     # Query to fetch the month and year an account was created along with the count of created accounts
#     creation_stats = db.session.query(
#         func.date_trunc('month', User.createdAt).label('month_year'),
#         func.count().label('total_accounts_created')
#     ).group_by('month_year').order_by('month_year').all()

#     # Serialize the results
#     serialized_stats = [{'month_year': stat[0], 'total_accounts_created': stat[1]} for stat in creation_stats]

#     return jsonify(serialized_stats)

if __name__ == "__main__":
    app.run(debug=False)
