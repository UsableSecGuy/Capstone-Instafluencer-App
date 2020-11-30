from sqlalchemy import Column, ARRAY, DateTime
import datetime
# String, Integer, Float, ARRAY, create_engine
from flask_sqlalchemy import SQLAlchemy
# import json
import os

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
!!NOTE you can change the database_filename variable to have multiple verisons
of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
Instafluencer
have id, username,full_name, profile_link, profile_pic_link,
followers, posts_per_week, engagement, hashtags
'''


class Instafluencer(db.Model):
    __tablename__ = 'instafluencer'

    id = Column(db.Integer, primary_key=True)
    username = Column(db.String, unique=True, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    profile_pic_link = db.Column(db.String, nullable=False)
    profile_link = db.Column(db.String, unique=True, nullable=False)
    followers = db.Column(db.Integer, nullable=False)
    posts_per_week = db.Column(db.Float, nullable=False)
    engagement = db.Column(db.Float, nullable=False)
    hashtags = db.Column(ARRAY(db.String), nullable=False)

    # also needs relationship to show models
    saved_instafluencers = db.relationship('Saved', backref='influencer',
                                                            lazy=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


'''
SavedInsta
have id, searcher_username, insta_fluencer_id, date_saved
'''


class SavedInsta(db.Model):
    __tablename__ = 'saved_insta'

    id = Column(db.Integer, primary_key=True)
    searcher_username = Column(db.String, unique=True, nullable=False)
    insta_fluencer_id = db.Column(db.Integer,
                                  db.ForeignKey('instafluencer.id'),
                                  nullable=False)
    date_saved = Column(DateTime, default=datetime.datetime.utcnow)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
