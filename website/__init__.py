from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, mkdir

ARICLE_WRITER_DB_NAME = '/databases/article_database.db'
EMAIL_SUBSCRIPTION_DB_NAME = '/databases/email_subscriptions.db'
UPLOAD_FOLDER = 'website/static/assets/'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'L&*$R@KWg,NB<ASWEMHfdbvalb32#"£~@'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite://{ARICLE_WRITER_DB_NAME}'
    app.config['SQLALCHEMY_BINDS'] = {'email_subcriptions' : f'sqlite://{EMAIL_SUBSCRIPTION_DB_NAME}'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    
    global db
    db = SQLAlchemy(app)
    
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
    if not path.exists('website' + EMAIL_SUBSCRIPTION_DB_NAME):
        db.create_all(bind='email_subcriptions')
    
def create_dir():
    required_dirs = ['article_covers', 'writer_pfps']
    for dir in required_dirs:
        if not path.exists(UPLOAD_FOLDER + dir):
            mkdir(UPLOAD_FOLDER + dir)