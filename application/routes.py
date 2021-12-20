from application import app
from flask import render_template
from application.models import My_Songs
from application.youtube_api import get_yt_search_results
from application import tab_scraper
from application.forms import RegisterForm

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

@app.route("/search")
def search_page():
    result_list = get_yt_search_results()
    tab_list = tab_scraper.get_tab_search_results()
    return render_template("search.html", items=result_list, tabs=tab_list)

@app.route("/my-songs")
def mysongs_page():
    mysongs = My_Songs.query.all()
    print(mysongs)
    return render_template("my-songs.html", songs=mysongs)

@app.route("/register")
def register_page():
    form = RegisterForm()
    return render_template("register.html", form=form)