from application import db, login_manager
from application import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer(), primary_key=True) 
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email_address = db.Column(db.String(length=50), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    saved_songs = db.relationship('My_Songs', backref='owned_user', lazy=True)
    wishlist = db.relationship('Wishlist', backref='owned_user', lazy=True)


    def get_id(self):
           return (self.user_id)


    @property
    def password(self):
        return self.password


    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')


    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
            

class My_Songs(db.Model):
    song_id = db.Column(db.Integer(), primary_key=True) 
    title = db.Column(db.String(length=50), nullable=False)
    tuning = db.Column(db.String(length=10))
    video_id = db.Column(db.String(length=200), unique=True)
    tab_url = db.Column(db.String(length=200), unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.user_id'))


    def __repr__(self):
        return f'Song {self.song}'


class Wishlist(db.Model):
    song_id = db.Column(db.Integer(), primary_key=True) 
    artist = db.Column(db.String(length=50), nullable=False)
    song = db.Column(db.String(length=50), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.user_id'))


    def __repr__(self):
        return f'Song {self.song}'