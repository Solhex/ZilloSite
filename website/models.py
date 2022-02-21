from . import db
from sqlalchemy.sql import func

class Writer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    picture_link = db.Column(db.String(200))
    articles = db.relationship('Article')

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(256))
    content = db.Column(db.String(5000), nullable=False)
    youtube_embed_link = db.Column(db.String(200))
    writer_id = db.Column(db.Integer, db.ForeignKey('writer.id'))