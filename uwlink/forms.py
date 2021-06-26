from flask_wtf import FlaskForm
from uwlink.models import User, Event
from mongoengine import DoesNotExist
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateTimeField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError, Email


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    email = StringField('Email', validators=[
        DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    # Functions named validate_<field> will be called to validate a specific field
    def validate_username(self, field):
        try:
            if User.objects.get(username=field.data):
                raise ValidationError('Username already in use.')
        except DoesNotExist:
            pass


class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    description = TextAreaField('Event Description', validators=[DataRequired()])
    tags = StringField('Tags (separate with spaces)')
    date = DateField('Date (YYYY-MM-DD)', format='%Y-%m-%d')
    time = TimeField('Time (HH:MM)', format='%H:%M')
    submit = SubmitField('Post Event')
