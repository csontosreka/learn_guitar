from enum import unique

from sqlalchemy.orm import backref
from application import db


class User(db.Model):
    user_id = db.Column(db.Integer(), primary_key=True) 
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email_address = db.Column(db.String(length=50), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    saved_songs = db.relationship('My_Songs', backref='owned_user', lazy=True)


class My_Songs(db.Model):
    song_id = db.Column(db.Integer(), primary_key=True) 
    artist = db.Column(db.String(length=50), nullable=False)
    song = db.Column(db.String(length=50), nullable=False)
    tab_type = db.Column(db.String(length=10), nullable=False)
    tuning = db.Column(db.String(length=10))
    yt_url = db.Column(db.String(length=200), nullable=False, unique=True)
    tab_url = db.Column(db.String(length=200), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.user_id'))

    def __repr__(self):
        return f'Song {self.song}'