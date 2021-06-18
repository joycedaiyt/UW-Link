from flask import Flask
from flask_mongoengine import MongoEngine
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

# MongoEngine is a library for easily working with MongoDB from Python. The classes in uwlink/models.py
# correspond to separate MongoDB collections (automatically created if not exists) and instances of those classes
# correspond to documents within those collections
#
# https://docs.mongoengine.org/guide/defining-documents.html
# https://docs.mongoengine.org/guide/querying.html
#
# Flask MongoEngine is a thin wrapper over MongoEngine which adds some convenient Flask-related features, like the
# get_or_404 method used in uwlink/routes.py
#
# http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/
db = MongoEngine()

bootstrap = Bootstrap()

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Configure Flask to connect to our MongoDB cluster
    #
    # In a production application, you would not hardcode the DB's username and password, but rather obtain them from
    # environment variables or some other configuration service
    #
    # https://security.stackexchange.com/questions/184021/managing-db-credentials-for-web-applications
    mongo_username = 'admin'
    mongo_password = 'admin'
    app.config['MONGODB_HOST'] = 'mongodb+srv://{}:{}@cluster0.ryror.mongodb.net/uwlink?retryWrites=true&w=majority'\
        .format(mongo_username, mongo_password)
    db.init_app(app)

    bootstrap.init_app(app)

    # Like the DB credentials, this should not be harcoded
    #
    # This is used by Flask for various tasks, like signing cookies
    app.config['SECRET_KEY'] = 'a super secret key'
    login_manager.init_app(app)

    # Register the API endpoints we defined in uwlink/routes.py
    from uwlink.routes import routes
    app.register_blueprint(routes)
    return app
