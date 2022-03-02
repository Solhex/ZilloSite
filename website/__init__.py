from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path, mkdir

ARICLE_WRITER_DB_NAME = '/databases/article_database.db'
EMAIL_SUBSCRIPTION_DB_NAME = '/databases/email_subscriptions.db'
EVENTS_DB_NAME = '/databases/events_database.db'
UPLOAD_FOLDER = 'website/static/assets/'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'L&*$R@KWg,NB<ASWEMHfdbvalb32#"£~@'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite://{ARICLE_WRITER_DB_NAME}'
    app.config['SQLALCHEMY_BINDS'] = {'email_subcriptions' : f'sqlite://{EMAIL_SUBSCRIPTION_DB_NAME}', 'events_database' : f'sqlite://{EVENTS_DB_NAME}'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    
    global db
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    
    db.init_app(app)
    
    from .views import views
    from .errorhandler import errorhandlermold
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(errorhandlermold, url_prefix='/errorpages')
    
    create_database(app)
    create_dir()
    
    return app

def create_database(app):
    if not path.exists('website' + ARICLE_WRITER_DB_NAME):
        db.create_all(app=app)
        
    for key in app.config['SQLALCHEMY_BINDS']:
        if not path.exists('website' + 'databases' + key + '.db'):
            db.create_all(bind=key)
    
def create_dir():
    required_dirs = ['article_covers', 'writer_pfps', 'event_covers']
    for dir in required_dirs:
        if not path.exists(UPLOAD_FOLDER + dir):
            mkdir(UPLOAD_FOLDER + dir)