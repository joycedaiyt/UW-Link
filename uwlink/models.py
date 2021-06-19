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
    events_joined = db.ListField(db.StringField())    #Includes events created
    joined_at = db.DateTimeField()

    # No need to include this in to_dict
    hashed_password = db.StringField()

    def to_dict(self):
        return {
            "owner_id": str(self.id),
            "username": self.username,
            "email": self.email,
            "events_joined": self.events_joined,
            "joined_at": self.joined_at
        }


class Event(db.Document):
    name = db.StringField()
    description = db.StringField()
    time = db.StringField()
    creator = db.stringField()
    participants = db.ListField(db.StringField())
    created_at = db.DateTimeField()

    def to_dict(self):
        return {
            "event_id": str(self.id),
            "name": self.name,
            "description": self.description,
            "creator": self.creator,
            "participants": self.participants,
            "created_at": self.created_at
        }

# class Pet(db.Document):
#     name = db.StringField()
#     type = db.StringField()
#     owner_id = db.StringField()
#
#     def to_dict(self):
#         return {
#             "pet_id": str(self.id),
#             "name": self.name,
#             "type": self.type,
#             "owner_id": self.owner_id
#         }
