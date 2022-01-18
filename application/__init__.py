from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mysongs.db'
app.config['SECRET_KEY'] = 'd2bb28095d76e0d2b045950f'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from application import routes