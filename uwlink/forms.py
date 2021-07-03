from flask_wtf import FlaskForm
from uwlink.models import User, Event
from mongoengine import DoesNotExist
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateTimeField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError, Email

class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    description = TextAreaField('Event Description', validators=[DataRequired()])
    tags = StringField('Tags (separate with spaces)')
    date = DateField('Date (YYYY-MM-DD)', format='%Y-%m-%d')
    time = TimeField('Time (HH:MM)', format='%H:%M')
    submit = SubmitField('Post Event')

class SearchForm(FlaskForm):
    tags = StringField('Tags', validators=[DataRequired()])
    submit = SubmitField('Search')
