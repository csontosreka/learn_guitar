from application import app
from flask import render_template, redirect, url_for
from application.models import My_Songs, User
from application.youtube_api import get_yt_search_results
from application import tab_scraper
from application.forms import RegisterForm
from application import db

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

@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                                email_address=form.email_address.data,
                                password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('home_page'))
    if form.errors != {}: #ha nincs hiba a validációnál üres dictionary-t kapunk
        for err_msg in form.errors.values():
            print(f'There was an error with creating a user: {err_msg}')
    return render_template("register.html", form=form)