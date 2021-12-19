from application import db

class My_Songs(db.Model):
    song_id = db.Column(db.Integer(), primary_key=True) 
    artist = db.Column(db.String(length=50), nullable=False)
    song = db.Column(db.String(length=50), nullable=False)
    tab_type = db.Column(db.String(length=10), nullable=False)
    tuning = db.Column(db.String(length=10))
    yt_url = db.Column(db.String(length=200), nullable=False, unique=True)
    tab_url = db.Column(db.String(length=200), nullable=False, unique=True)

    def __repr__(self):
        return f'Song {self.song}'