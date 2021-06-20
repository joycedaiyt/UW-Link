import datetime

from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for
from flask_login import UserMixin, current_user, login_required, login_user
from mongoengine.errors import DoesNotExist
from uwlink import login_manager
from uwlink.forms import LoginForm, SignupForm, EventForm
from uwlink.models import User, Event
from werkzeug.security import check_password_hash, generate_password_hash


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
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    events_joined=[],
                    events_created=[],
                    joined_at=datetime.datetime.now(),
                    hashed_password=generate_password_hash(form.password.data))
        user.save()
        flash('You have been signed up!')
        return redirect(url_for('.login'))
    return render_template('signup.html', form=form)


@routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.objects.get(username=form.username.data)
            if check_password_hash(user.hashed_password, form.password.data):
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
        event = Event(
            name=form.name.data,
            description=form.description.data,
            time=form.time.data,
            creator=user.username,
            participants=[],
            created_at=datetime.datetime.now())
        event.save()
        user.events_created.append(str(event.id))
        user.save()
        flash('Event created successfully!')
        return redirect(url_for('.login')) #to be changed to homepage
    return render_template('create.html', form=form)
