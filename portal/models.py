#!/usr/bin/python
from hashlib import sha512
import string
import random
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def generate_password():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for i in range(0, 16))


class School(db.Model):
    __tablename__ = 'schools'
    abbrev = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    passwd = db.Column(db.String, nullable=False)

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
