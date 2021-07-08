from datetime import datetime

from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for
from flask_login import UserMixin, current_user, login_required, login_user, logout_user
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
                flash('Username already exist')
                return redirect(url_for('.login'))
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
    if current_user.is_authenticated:
        return redirect(url_for('.feed'))
    form = request.form
    if request.method == 'POST':
        try:
            user = User.objects.get(username=form.get("loginUser"))
            if check_password_hash(user.hashed_password, form.get("loginPassword")):
                user = LoginUser(user)
                login_user(user)
                flash('You have logged in!')
                return redirect(url_for('.feed')) # changed to homepage
        except DoesNotExist:
            pass
    return render_template('login.html', form=form)


# creates a new event
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
        return redirect(url_for('.feed')) #to be changed to homepage
    return render_template('create.html', form=form)


@routes.route('/feed', methods=['GET'])
@login_required
def feed():
    event_list = list(Event.objects)
    return render_template('feed.html', event_list=event_list, 
                            results=False, user=User.objects.get(id=current_user.id))


# search events
@routes.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        data = [None] * 5
        data[0] = form.name.data
        data[1] = form.tags.data
        data[2] = form.date_from.data
        data[3] = form.date_to.data
        data[4] = form.display_past_events.data
        return redirect(url_for('.result', data=data))
    return render_template('search.html', form=form)


# display search results for the given data      
@routes.route('/result/<data>', methods=['GET'])
@login_required
def result(data):
    content = data.strip('][').split(', ')
    fields = [None] * len(content)
    for i in range(0,2):
        fields[i] = content[i][1:len(content[i])-1]
    for i in range(2,len(content)):
        fields[i] = content[i]
    event_list = []
    if fields[0] == "" and fields[1] == "":
        event_list = list(Event.objects)
    else:
        search_names = fields[0]
        search_tags = fields[1]
        # and search for event names (>= 2/3 matching)
        names = []
        for name in search_names.split():
            if name not in names:
                names.append(name)
        if len(names) > 0:
            for event in list(Event.objects):
                count = 0
                for name in names:
                    if name in event.name:
                        count += 1
                if count >= 2/3 * len(names):
                    event_list.append(event)
        # or search for event tags
        tags = []
        for tag in search_tags.split():
            if tag not in tags:
                tags.append(tag)
        for tag in tags:
            try:
                TAG = Tag.objects.get(name=tag)
                events = TAG.events
                for event_id in events:
                    event = Event.objects.get(id=ObjectId(event_id))
                    if event not in event_list:
                        event_list.append(event)
            except DoesNotExist:
                pass
    # filters by time
    event_list.sort(key=lambda event: event.time, reverse=True)
    idx = 2
    if fields[idx] != 'None':
        search_time = fields[idx][14:] + '-' + fields[idx+1] + '-' + fields[idx+2][0:len(fields[idx+2])-1]
        time_from = datetime.strptime(search_time, '%Y-%m-%d')
        newlist = []
        for event in event_list:
            if event.time.date() >= time_from.date():
                newlist.append(event)
            else:
                break
        event_list = newlist
        idx += 3
    else:
        idx += 1
    if fields[idx] != 'None':
        event_list.reverse()
        search_time = fields[idx][14:] + '-' + fields[idx+1] + '-' + fields[idx+2][0:len(fields[idx+2])-1]
        time_to = datetime.strptime(search_time, '%Y-%m-%d')
        newlist = []
        for event in event_list:
            if event.time.date() <= time_to.date():
                newlist.append(event)
            else:
                break
        event_list = newlist
        idx += 3
        event_list.reverse()
    else:
        idx += 1
    if fields[idx] == 'False':
        time = datetime.now()
        newlist = []
        for event in event_list:
            if event.time >= time:
                newlist.append(event)
            else:
                break
        event_list = newlist
    event_list.reverse()
    return render_template('feed.html', event_list=event_list,
                            results=True, user=User.objects.get(id=current_user.id))


@routes.route('/profile/<username>', methods=['GET'])
@login_required
def profile(username):
    user = User.objects.get(username=username)
    events_created = []
    for event_id in user.events_created:
        event = Event.objects.get(id=event_id)
        events_created.append(event)
    events_joined = []
    for event_id in user.events_joined:
        event = Event.objects.get(id=event_id)
        events_joined.append(event)
    return render_template('profile.html', name = user.username,
                           email = user.email,
                           join = user.joined_at,
                           events_created = events_created,
                           events_joined = events_joined)


@routes.route('/account', methods=['GET'])
@login_required
def account():
    events_created = []
    for event_id in current_user.user.events_created:
        event = Event.objects.get(id = event_id)
        events_created.append(event)
    events_joined = []
    for event_id in current_user.user.events_joined:
        event = Event.objects.get(id = event_id)
        events_joined.append(event)
    return render_template('profile.html', name = current_user.user.username,
                           email = current_user.user.email,
                           join = current_user.user.joined_at,
                           events_created = events_created,
                           events_joined = events_joined)


@routes.route('/join', methods=['POST'])
@login_required
def join():
    event_id = request.form.get("event_id")
    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=current_user.id)
    user.events_joined.append(str(event.id))
    user.save()
    event.participants.append(str(user.username))
    event.save()
    flash('Joined!')
    return redirect(url_for('.feed'))


@routes.route('/leave', methods=['POST'])
@login_required
def leave():
    event_id = request.form.get("event_id")
    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=current_user.id)
    user.events_joined.remove(str(event.id))
    user.save()
    event.participants.remove(str(user.username))
    event.save()
    flash('Left!')
    return redirect(url_for('.feed'))


@routes.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))
