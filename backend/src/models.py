from sqlalchemy import Column, String, Integer, ARRAY, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
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
Instafluencer
have id, username,full_name, profile_link, profile_pic_link,
followers, posts_per_week, engagement, hashtags
'''
class Instafluencer(db.Model):
    __tablename__ = 'instafluencer'

    id = Column(db.Integer, primary_key=True)
    username = Column(db.String, unique=True)
    full_name = db.Column(db.String, nullable=False)
    profile_pic_link = db.Column(db.String, nullable=False)
    profile_link = db.Column(db.String, unique=True)
    followers = db.Column(db.Integer)
    posts_per_week = db.Column(db.Integer)
    engagement = db.Column(db.String)
    hashtags = ARRAY(db.String)

    #also needs relationship to show models
    saved_instafluencers = db.relationship('Saved', backref='influencer', lazy=True)

'''
SavedInsta
have id, username, insta_fluencer_id, date_saved
'''
class SavedInsta(db.Model):
    __tablename__='saved_insta'

    id = Column(db.Integer, primary_key=True)
    username = Column(db.String, unique=True)
    insta_fluencer_id = db.Column(db.Integer, db.ForeignKey('instafluencer.id'), nullable=False)
    date_saved = Column(db.DateTime)
