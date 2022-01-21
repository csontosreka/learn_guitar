from application import app
from flask import render_template, redirect, url_for, flash
from application.models import My_Songs, User
from application.youtube_api import get_yt_search_results
from application import tab_scraper
from application.forms import RegisterForm, LoginForm
from application import db
from flask_login import login_user,logout_user, login_required


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
@login_required
def mysongs_page():
    mysongs = My_Songs.query.all()
    return render_template("my-songs.html", songs=mysongs)


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                                email_address=form.email_address.data,
                                password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('login_page'))

    if form.errors != {}: #ha nincs hiba a validációnál üres dictionary-t kapunk
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    print(form.errors)

    if form.is_submitted():
        print("Submitted")

    if form.validate():
        print("Valid")

    print(form.errors)

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route("/logout")
def logout_page():
    logout_user()
    flash(f'You are logged out!', category='info')
    return redirect(url_for('home_page'))