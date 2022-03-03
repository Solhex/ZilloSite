from . import db
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

class Subscription(db.Model):
    __bind_key__ = 'email_subcriptions'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    datetime_joined = db.Column(db.DateTime(timezone=True), default=func.now())

class Event(db.Model):
    __bind_key__ = 'event_database'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    address1 = db.Column(db.String(256), nullable=False)
    address2 = db.Column(db.String(256))
    city = db.Column(db.String(256), nullable=False)
    county = db.Column(db.String(256))
    country = db.Column(db.String(256), nullable=False)
    postcode = db.Column(db.String(10), nullable=False)
    datetime_end = db.Column(db.DateTime(timezone=True))
    datetime_start = db.Column(db.DateTime(timezone=True))
    datetime_posted = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())

class Volunteer(db.Model):
    __bind_key__ = 'volunteer_database'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    address1 = db.Column(db.String(256), nullable=False)
    address2 = db.Column(db.String(256))
    city = db.Column(db.String(256), nullable=False)
    county = db.Column(db.String(256))
    country = db.Column(db.String(256), nullable=False)
    postcode = db.Column(db.String(10), nullable=False)
    datetime_end = db.Column(db.DateTime(timezone=True))
    datetime_start = db.Column(db.DateTime(timezone=True))
    datetime_posted = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
