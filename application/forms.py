from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from application.models import User


class RegisterForm(FlaskForm):


    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try again.')


    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email address already exists! Please try again.')


    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


class AddSongForm(FlaskForm):
    artist = StringField(label='Artist:', validators=[DataRequired()])
    title = StringField(label='Title:', validators=[DataRequired()])
    submit = SubmitField(label='Add Song')


class SearchForm(FlaskForm):
    artist = StringField(label='Artist', validators=[DataRequired()])
    song = StringField(label='Song title', validators=[DataRequired()])
    submit = SubmitField('')