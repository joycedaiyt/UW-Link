from flask_wtf import FlaskForm
from uwlink.models import User, Event
from mongoengine import DoesNotExist
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateTimeField, DateField, TimeField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError, Email, Optional

class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    description = TextAreaField('Event Description', validators=[DataRequired()])
    tags = StringField('Tags (separate with spaces)')
    date = DateField('Date (YYYY-MM-DD)', format='%Y-%m-%d')
    time = TimeField('Time (HH:MM)', format='%H:%M')
    submit = SubmitField('Post Event')

class SearchForm(FlaskForm):
    name = StringField('Event Name')
    tags = StringField('Tags')
    date_from = DateField('From (YYYY-MM-DD)', validators=[Optional()])
    date_to = DateField('To (YYYY-MM-DD)', validators=[Optional()])
    display_past_events = BooleanField('Display Past Events?')
    submit = SubmitField('Search')

class UpdateForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=1, max=64)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit1 = SubmitField('Update')

    def validate_username(self, username):
        user = User.objects.get(id=current_user.id)
        if username.data != user.username:
            try:
                user = User.objects.get(username=username.data)
                if user:
                    raise ValidationError('That username is taken. Please choose a different one.')
            except DoesNotExist:
                pass

    def validate_email(self, email):
        user = User.objects.get(id=current_user.id)
        if email.data != user.email:
            try:
                user = User.objects.get(email=email.data)
                if user:
                    raise ValidationError('That email is taken. Please choose a different one.')
            except DoesNotExist:
                pass

class UpdatePassword(FlaskForm):
    oldpassword = PasswordField('Old Password',
                        validators=[DataRequired()])
    newpassword = PasswordField('New Password',
                        validators=[DataRequired(), Length(min=6, max=64), Regexp('(?=.*\d)(?=.*[a-z])')])
    confirmpassword = PasswordField('Confirm Password',
                        validators=[DataRequired()])
    submit2 = SubmitField('Update')



