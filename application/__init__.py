from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mysongs.db'
app.config['SECRET_KEY'] = 'd2bb28095d76e0d2b045950f'
db = SQLAlchemy(app)

from application import routes