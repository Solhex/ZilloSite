from . import db                    # from __init__.py it imports SQLAlchemy(app)
from sqlalchemy.sql import func     # imports the func which will be used to get the current datetime

class Writer(db.Model):                                     # defines the writer table and uses db.model to inform that it comforms to the sqlalchemy module
    id = db.Column(db.Integer, primary_key=True)            # creates a column called id, as a integer, set as the primary key, meaning it'll increment every entry addition
    firstname = db.Column(db.String(50), nullable=False)    # creates a column called firstname, as a string with the max string length of 50, and make it required to be filled in
    lastname = db.Column(db.String(50), nullable=False)     # creates a column called lastname, as a string with the max string length of 50, and make it required to be filled in
    picture_link = db.Column(db.Boolean(), default=False)   # creates a column called picture_link, as a boolean value (True / False), with the default value of False
    datetime_joined = db.Column(db.DateTime(timezone=True), default=func.now()) # creates a column called datetime_joined, as a datetime python value, with the default value of the current datetime
    articles = db.relationship('Article')                   # creates a column of relationships between the article table

class Article(db.Model):                                    # defines the article table and uses db.model to inform that it comforms to the sqlalchemy module
    id = db.Column(db.Integer, primary_key=True)
    datetime_posted = db.Column(db.DateTime(timezone=True), default=func.now())
    datetime_created = db.Column(db.DateTime(timezone=True), default=func.now())
    title = db.Column(db.String(100), nullable=False)       # creates a column called title, as a string with the max string length of 100, required to be filled in
    description = db.Column(db.String(256))                 # creates a column called description, as a string with the max string length of 256, not required to be filled in
    content = db.Column(db.String(5000), nullable=False)
    youtube_embed_link = db.Column(db.String(200))
    writer_id = db.Column(db.Integer, db.ForeignKey('writer.id'))               # creates a foreignkey between the writer table, with the writer id as the foreignkey

class Subscription(db.Model):                               # defines the subscription table and uses db.model to inform that it comforms to the sqlalchemy module
    __bind_key__ = 'email_subcriptions'                     # __bind_key__ is only for additional databases defined within app.config['SQLALCHEMY_BINDS'] without that it will be added to the primary database as a table, this binds it to the email_subcriptions database
    id = db.Column(db.Integer, primary_key=True)            
    email = db.Column(db.String(50), nullable=False, unique=True)               # creates a column called email, as a string with the max string length of 50, required to be filled in, and cannot have duplicates
    datetime_joined = db.Column(db.DateTime(timezone=True), default=func.now()) # creates a column called datetime_joined, as a datetime python value, with the default value of the current datetime

class Event(db.Model):                                      # defines the event table and uses db.model to inform that it comforms to the sqlalchemy module
    __bind_key__ = 'event_database'                         # __bind_key__ binds it to the event_database database within app.config['SQLALCHEMY_BINDS']
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

class Volunteer(db.Model):                                  # defines the volunteer table and uses db.model to inform that it comforms to the sqlalchemy module
    __bind_key__ = 'volunteer_database'                     # __bind_key__ binds it to the volunteer_database database within app.config['SQLALCHEMY_BINDS']
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
