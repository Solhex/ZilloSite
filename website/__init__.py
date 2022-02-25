from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

ARICLE_WRITER_DB_NAME = 'article_database.db'
EMAIL_SUBSCRIPTION_DB_NAME = 'email_subscriptions.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'L&*$R@KWg,NB<ASWEMHfdbvalb32#"£~@'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///databases/{ARICLE_WRITER_DB_NAME}'
    app.config['SQLALCHEMY_BINDS'] = {'email_subcriptions' : f'sqlite:///databases/{EMAIL_SUBSCRIPTION_DB_NAME}'}
    
    global db
    db = SQLAlchemy(app)
    
    db.init_app(app)
    
    from .views import views
    
    app.register_blueprint(views, url_prefix='/')
    
    create_database(app)
    
    return app

def create_database(app):
    if not path.exists('website/databases/' + ARICLE_WRITER_DB_NAME):
        db.create_all(app=app)
    if not path.exists('website/databases/' + EMAIL_SUBSCRIPTION_DB_NAME):
        db.create_all(bind='email_subcriptions')
    