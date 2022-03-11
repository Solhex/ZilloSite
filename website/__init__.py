from flask import Flask                             # imports Flask from flask, done this way as so I dont have to use flask.Flask every time I mention this function
from flask_sqlalchemy import SQLAlchemy             # imports SQLAlchemy from flask_sqlalchemy, flasks version of SQLAlchemy that more better accomodates for flasks functions
from flask_migrate import Migrate                   # imports Migrate from flask_migrate, this module uses Alembic to reconfigure existing databases if editing them is so required refer to the readme.md to learn how to
from os import path, mkdir                          # imports path and mkdir from os, path is used to create paths compatible with multiple oses, mkdir justs makes directories when used

ARICLE_WRITER_DB_NAME = '/databases/article_database.db'            # creates a simple variable with the article database relative path within, capitalized to remind other editors that it should be treated like a constant
EMAIL_SUBSCRIPTION_DB_NAME = '/databases/email_subscriptions.db'    # creates a simple variable with the email subscription database relative path within
EVENTS_DB_NAME = '/databases/event_database.db'                     # creates a simple variable with the events database relative path within
VOLUNTEER_DB_NAME = '/databases/volunteer_database.db'              # creates a simple variable with the volunteer database relative path within
UPLOAD_FOLDER = 'website/static/assets/'                            # creates a simple variable with the upload folder relative path within

def create_app():                                                                   # creates a function to be called by main.py and will start the rest of the program / website / server
    app = Flask(__name__)                                                           # creates a flask instance with the name value of __name__, __name__ is recommended if a single module is being used and for debugging, using a hardcoded name is only recommended when using a package, without __name__ debugging is harder as debug mode will not reference the file the error was in
    app.config['SECRET_KEY'] = 'L&*$R@KWg,NB<ASWEMHfdbvalb32#"£~@'                  # this is used as a seed so cryptographic components can use this to sign cookies and other things, change this before post production and make sure to hide the key string changing the string post production will not allow you to decrypt any previous encrypted media without the same key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite://{ARICLE_WRITER_DB_NAME}'     # creates a link / bind to the primary database with sqlite

    app.config['SQLALCHEMY_BINDS'] = {                                              # creates uses a dictionary to link / bind to additional databases
        'email_subcriptions' : f'sqlite://{EMAIL_SUBSCRIPTION_DB_NAME}',            # links / binds the email_subcriptions database
        'event_database' : f'sqlite://{EVENTS_DB_NAME}',                            # links / binds the event_database database
        'volunteer_database' : f'sqlite://{VOLUNTEER_DB_NAME}'                      # links / binds the volunteer_database database
        }                                                                           # ends the dictionary

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER                     # links the upload folder, any files uploaded to the site will be here
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024             # sets the maximum upload size to 16mb, formatted like this for better modification
    
    global db                                       # creates the variable db to globally, aka it'll exist out of the function
    db = SQLAlchemy(app)                            # activates initializes SQLAlchemy's code and sets db to be the container
    migrate = Migrate(app, db)                      # activates initializes Migrate's code and passes though app and db for later use with flask db, see readme.md
    
    db.init_app(app)                                # initializes db / SQLAlchemy and passes though app / flask
    
    from .views import views                        # imports views and from the same directory
    from .errorhandler import errorhandlermold      # imports errorhandler and from the same directory
    
    app.register_blueprint(views, url_prefix='/')                                   # registers the views blueprint and sets the route "/" as the route folder
    app.register_blueprint(errorhandlermold, url_prefix='/errorpages')              # registers the errorhandlermold blueprint and sets the route "/errorpages" as the route folder
    
    create_database(app)                            # calls the create_database function and passes though app 
    create_dir()                                    # calls the create_dir function
    
    return app                                      # returns app

def create_database(app):                                           # creates a function with a required passed variable
    if not path.exists('website' + ARICLE_WRITER_DB_NAME):          # checks if the file at /databases/article_database.db exists, if not then it executes the code below
        db.create_all(app=app)                                      # uses flask_sqlalchemy's create_all function to create the file
        
    for key in app.config['SQLALCHEMY_BINDS']:                      # creates a for loop for each key within the app.config['SQLALCHEMY_BINDS']
        if not path.exists('website' + 'databases' + key + '.db'):  # checks if the database for that key exists, if not then it executes the code below, the database' name and the key's name must be the same for this to work
            db.create_all(bind=key)                                 # uses flask_sqlalchemy's create_all function to create the file for the bind
    
def create_dir():                                                                   # creates a function
    required_dirs = {'article_covers', 'event_covers', 'volunteer_covers'}          # creates a set of required directories, sets are not organized nor can contain duplicates
    for dir in required_dirs:                                                       # creates a loop for each item within the list
        if not path.exists(UPLOAD_FOLDER + dir):                                    # checks if it exists, if not then it executes the code below
            mkdir(UPLOAD_FOLDER + dir)                                              # creates that directory