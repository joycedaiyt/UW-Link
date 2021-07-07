from flask_wtf import FlaskForm
from uwlink.models import User, Event
from mongoengine import DoesNotExist
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
