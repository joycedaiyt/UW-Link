from uwlink import db

# The model classes here (anything which inherits from db.Document) represent data stored in the database
#
# Each class also has a to_dict method, which returns a dictionary of data that we intend to send back to the user in
# API responses. Having this method decouples the schema of the database from the schema of the API responses
#
# I got this idea from UWFlow (which is also a Flask+MongoDB project)
#
# https://github.com/UWFlow/rmc/blob/00bcc1450ffbec3a6c8d956a2a5d1bb3a04bfcb9/models/course.py


class User(db.Document):
    # Setting unique=True causes MongoEngine to create this collection with a unique index on this field
    #
    # https://docs.mongodb.com/manual/core/index-unique/
    username = db.StringField(unique=True)
    email = db.StringField(unique=True)
    events_joined = db.ListField(db.StringField())
    events_created = db.ListField(db.StringField())
    joined_at = db.DateTimeField()

    # No need to include this in to_dict
    hashed_password = db.StringField()

    def to_dict(self):
        return {
            "owner_id": str(self.id),
            "username": self.username,
            "email": self.email,
            "events_joined": self.events_joined,
            "events_created": self.events_created,
            "joined_at": self.joined_at
        }


class Event(db.Document):
    name = db.StringField()
    description = db.StringField()
    tags = db.ListField(db.StringField())
    time = db.DateTimeField()
    creator = db.StringField()
    participants = db.ListField(db.StringField())
    created_at = db.DateTimeField()

    def to_dict(self):
        return {
            "event_id": str(self.id),
            "name": self.name,
            "description": self.description,
            "time": self.time,
            "creator": self.creator,
            "participants": self.participants,
            "created_at": self.created_at
        }


class Tag(db.Document):
    name = db.StringField()
    events = db.ListField(db.StringField())

    def to_dict(self):
        return {
        "tag_id": str(self.id),
        "name": self.name,
        "events": self.events
        }
