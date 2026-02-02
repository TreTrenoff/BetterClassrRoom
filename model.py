from datetime import datetime, timezone
from db import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f'<User {self.username}> - {self.created_at} : {self.email}, {self.id}'

class Rank(db.Model):
    __tablename__ = 'rank'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rank_value = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref=db.backref('ranks', lazy=True))