from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = 'article_database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'L&*$R@KWg,NB<ASWEMHfdbvalb32#"£~@'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///databases/{DB_NAME}'

    db.init_app(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import Article, Writer
    
    create_database(app)
    
    return app

def create_database(app):
    if not path.exists('website/Databases/' + DB_NAME):
        db.create_all(app=app)