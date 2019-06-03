#!/usr/bin/python
from hashlib import sha512
import string
import random
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, login_manager

db = SQLAlchemy()
login_manager = LoginManager()

def generate_password():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for i in range(0, 16))

@login_manager.user_loader
def load_user(abbrev):
    return School.query.get(abbrev)

class School(UserMixin, db.Model):
    __tablename__ = 'schools'
    abbrev = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    passwd = db.Column(db.String, nullable=False)

    def get_id(self):
        return self.abbrev

class Venue(db.Model):
    __tablename__ = 'venues'
    name = db.Column(db.String, primary_key=True)

class Event(db.Model):
    __tablename__ = 'events'
    name = db.Column(db.String, primary_key=True)
    description = db.Column(db.String, nullable=False)
    venue = db.Column(db.String, db.ForeignKey("venues.name"), nullable=False)
    timings = db.Column(db.String, nullable=False)


class EventRegistrationEntry(db.Model):
    __tablename__ = 'events_registration'
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String, db.ForeignKey('events.name'), nullable=False)
    school_name = db.Column(db.String, db.ForeignKey('schools.abbrev'), nullable=False)
