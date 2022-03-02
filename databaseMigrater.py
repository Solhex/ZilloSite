from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///website/databases/article_database.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from sqlalchemy.sql import func

class Writer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    picture_link = db.Column(db.Boolean(), default=False)
    datetime_joined = db.Column(db.DateTime(timezone=True), default=func.now())
    articles = db.relationship('Article')

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime_posted = db.Column(db.DateTime(timezone=True), default=func.now())
    datetime_created = db.Column(db.DateTime(timezone=True), default=func.now())
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(256))
    content = db.Column(db.String(5000), nullable=False)
    youtube_embed_link = db.Column(db.String(200))
    writer_id = db.Column(db.Integer, db.ForeignKey('writer.id'))