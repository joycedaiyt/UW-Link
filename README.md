# Flask Mongo Sample

This sample app stores data for pets and owners. A pet has one owner, while an owner may have many pets. This is the same relationship between events and users in your UW Link project!

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

## Authentication
There is a great guide for setting up authentication with Flask here: https://testdriven.io/blog/web-authentication-methods/

I would recommend looking at the token-based authentication.
