**UW Link**

UW Link is a web app that provides a platform for Waterloo students to connect socially. This app will allow users to advertise events that they want to hold, and others can join in. Events can include video game sessions, sports tournaments, study buddies, connecting people for side projects, etc. Users can also find and meet people with similar interests and start coffee chats.

## Setup and Running

These instructions are Linux/Mac specific - Windows probably works too.

To setup your virtualenv:
```python
# https://docs.python.org/3/library/venv.html
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

To run the app:
```python
python3 run.py
```

To deactivate your virtualenv:
```python
deactivate
```

To reactivate your virtualenv:
```python
source venv/bin/activate
```

You can hit any of the endpoints with an HTTP client like Postman. If you have any questions, ping me.
