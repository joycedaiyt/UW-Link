from datetime import datetime

from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for
from flask_login import UserMixin, current_user, login_required, login_user
from mongoengine.errors import DoesNotExist
from uwlink import login_manager
from uwlink.forms import EventForm, SearchForm
from uwlink.models import User, Event, Tag
from werkzeug.security import check_password_hash, generate_password_hash
from bson.objectid import ObjectId

# In Flask, a blueprint is just a group of related routes (the functions below), it helps organize your code
routes = Blueprint('api', __name__)


class LoginUser(UserMixin):
    def __init__(self, user):
        self.id = user.id
        self.user = user


@login_manager.user_loader
def user_loader(user_id):
    try:
        user = User.objects.get(id=user_id)
        return LoginUser(user)
    except DoesNotExist:
        return None


# Signup creates a new user. Note that we store a HASH of the user's password - this is a common practice. On login,
# the provided password will be hashed, and that hash will be compared to the stored hash for the user
#
# https://en.wikipedia.org/wiki/Cryptographic_hash_function#Password_verification
@routes.route('/signup', methods=['GET', 'POST'])
def signup():
    form = request.form
    if request.method == 'POST':
        try:
            if User.objects.get(username=form.get("signupUser")):
                return "User name already exist"
        except DoesNotExist:
            pass
        user = User(username=form.get("signupUser"),
                    email=form.get("signupEmail"),
                    events_joined=[],
                    events_created=[],
                    joined_at=datetime.now(),
                    hashed_password=generate_password_hash(form.get("signupPassword")))
        user.save()
        flash('You have been signed up!')
        return redirect(url_for('.login'))
    return render_template('login.html', form=form)


@routes.route('/login', methods=['GET', 'POST'])
def login():
    form = request.form
    if request.method == 'POST':
        try:
            user = User.objects.get(username=form.get("loginUser"))
            if check_password_hash(user.hashed_password, form.get("loginPassword")):
                user = LoginUser(user)
                login_user(user)
                return "logged in"
        except DoesNotExist:
            pass
    return render_template('login.html', form=form)


@routes.route('/event', methods=['GET', 'POST'])
@login_required
def create():
    form = EventForm()
    if form.validate_on_submit():
        user = User.objects.get(id=current_user.id)
        form_date = str(form.date.data)
        form_time = str(form.time.data)
        time = datetime.strptime(form_date + form_time, '%Y-%m-%d%H:%M:%S')
        content = form.tags.data
        tags = []
        for word in content.split():
            if word not in tags:
                tags.append(word)
        event = Event(
            name=form.name.data,
            description=form.description.data,
            tags=tags,
            time=time,
            creator=user.username,
            participants=[],
            created_at=datetime.now())
        event.save()
        user.events_created.append(str(event.id))
        user.save()
        for tag in tags:
            try:
                tag = Tag.objects.get(name=tag)
            except DoesNotExist:
                tag = Tag(name=tag, events=[])
            tag.events.append(str(event.id))
            tag.save()
        flash('Event created successfully!')
        return redirect(url_for('.cards')) #to be changed to homepage
    return render_template('create.html', form=form)


@routes.route('/feed', methods=['GET'])
@login_required
def cards():
    event_list = list(Event.objects)
    return render_template('cards-page.html', event_list=event_list)


@routes.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        content = form.tags.data
        return redirect(url_for('.result', content=content))
    return render_template('search.html', form=form)

                
@routes.route('/result/<content>', methods=['GET'])
@login_required
def result(content):
    tags = []
    for tag in content.split():
        if tag not in tags:
            tags.append(tag)
    event_list = []
    for tag in tags:
        try:
            ttag = Tag.objects.get(name=tag)
            events = ttag.events
            for event_id in events:
                event = Event.objects.get(id=ObjectId(event_id))
                if event not in event_list:
                    event_list.append(event)
        except DoesNotExist:
            pass
    return render_template('result.html', event_list=event_list)
