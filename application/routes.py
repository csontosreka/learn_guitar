from application import app
from flask import render_template, redirect, url_for, flash, request
from application.models import My_Songs, Wishlist, User
from application.youtube_api import get_yt_search_results
from application import tab_scraper
from application.forms import RegisterForm, LoginForm, AddSongForm, SearchForm
from application import db
from flask_login import login_user,logout_user, login_required, current_user


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/search", methods=["GET", "POST"])
def search_page():
    form = SearchForm()
    if form.validate_on_submit():
        artist = form.artist.data
        song = form.song.data
        search_query = artist + ' - ' + song
        tab_list = tab_scraper.get_tab_search_results(artist, song)
    else:
        tab_list = []
        search_query = ''
    
    return render_template("search.html",form=form, query=search_query, tabs=tab_list)


@app.route("/tab", methods=["GET", "POST"])
def tab_page():
    tab_url = request.form.get('tab_url')
    title = request.form.get('title')
    tab = request.form.get('tab')

    if title is None:
        title = request.form.get('query').title()    

    if tab is None:
        tab = tab_scraper.get_tab(tab_url)['tab']
    else:
        print("Successfully read tabs from database")
    
    tab_data = tab_scraper.get_tab(tab_url)

    videos = get_yt_search_results(title)
    video_url = request.form.get('video_url')
    if video_url:
        video_id = video_url.replace('https://www.youtube.com/watch?v=', '')
    else:
        video_id = ''

    return render_template("tab.html", title=title, tab=tab, chords=tab_data['chord_list'], 
                            tab_url=tab_url, videos=videos, video_id=video_id, tuning=tab_data['tuning'])


@app.route("/my-songs")
@login_required
def mysongs_page():
    mysongs = My_Songs.query.filter_by(owner=current_user.user_id)
    return render_template("my-songs.html", songs=mysongs)


@app.route("/save",  methods=["GET", "POST"])
@login_required
def save_page(): 
    title = request.form.get('title')

    artist = title.split(' - ')[0]
    song = title.split(' - ')[1]
    
    tuning = request.form.get('tuning')
    tab_url = request.form.get('tab_url')
    tab = request.form.get('tab')
    video_id = request.form.get('video_id')

    song_to_create = My_Songs(artist=artist, song=song, tuning=tuning, tab_url=tab_url, video_id=video_id, tab=tab,
                                owner=current_user.user_id)
                                
    if My_Songs.query.filter_by(artist=artist, song=song, tuning=tuning, tab_url=tab_url, video_id=video_id, tab=tab,
                                owner=current_user.user_id).first() is None:

        if Wishlist.query.filter_by(artist=artist, song=song, owner=current_user.user_id).first() is not None:
            flash("This song is on your Wishlist too.", category='info')

        db.session.add(song_to_create)
        db.session.commit()
        flash('Song added successfully!', category='success')
    else: 
        flash('Cannot save song, or song is already added to your My Songs list.', category='danger')

    return redirect(url_for('mysongs_page'))


@app.route("/wishlist", methods=["GET", "POST"])
@login_required
def wishlist_page():
    form = AddSongForm()
    print(form.errors)

    if form.validate_on_submit() and request.method == "POST":
        song_to_create = Wishlist(artist=str(form.artist.data).title(),
                                song=str(form.title.data).title(),
                                owner=current_user.user_id)
        if Wishlist.query.filter_by(artist=str(form.artist.data).title(),
                                song=str(form.title.data).title(),
                                owner=current_user.user_id).first() is None:
            db.session.add(song_to_create)
            db.session.commit()
            flash('Song added successfully!', category='success')

        else:
            flash('Cannot save song, or song is already added to your wishlist', category='danger')

    wishlist = Wishlist.query.filter_by(owner=current_user.user_id)
    
    return render_template("wishlist.html", songs=wishlist, form=form)


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

    if form.errors != {}: #ha nincs hiba a valid??ci??n??l ??res dictionary-t kapunk
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
            flash('Username and password does not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route("/logout")
def logout_page():
    logout_user()
    flash(f'You are logged out!', category='info')
    return redirect(url_for('home_page'))
    

@app.route("/delete", methods=["GET", "POST"])
def delete_song_page():
    database = request.form.get('database')

    if database == 'Wishlist':
        row = request.form.get('song_to_delete').split(', ')
        artist = row[0]
        song = row[1]
        entry = Wishlist.query.filter_by(artist=artist, song=song, owner=current_user.user_id).first()
        page = 'wishlist_page'
    
    if database == 'My_Songs':
        row = request.form.get('song_to_delete').split(' - ')
        artist = row[0]
        song = row[1]
        entry = My_Songs.query.filter_by(artist=artist, song=song, owner=current_user.user_id).first()
        page = 'mysongs_page'
    
    if entry is not None:
        db.session.delete(entry)
        db.session.commit()
        flash(f'Song successfully deleted from {database}!', category='success')
    else:
        flash('Something went wrong! Cannot delete song', category='danger')

    return redirect(url_for(page))