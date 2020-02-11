#!/usr/bin/python

from flask import Flask, render_template, request
from models import *
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///portal'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db.init_app(app)


def generate_password():
    	chars = string.ascii_letters + string.digits
    	return ''.join(random.choice(chars) for i in range(0, 16))

def populate_schools():
	logs = []
	with open('source-csvs/schools.csv', 'r') as f:
		reader = csv.reader(f, delimiter=',')
		count = 0
		for abbrev, name in reader:
			if count == 0:
				logs.append([abbrev, name, ""])
				count += 1
				continue
			password = generate_password()
			school = School(abbrev=abbrev,
					   name=name,
					   passwd=sha512(password.encode('utf-8')).hexdigest())
			db.session.add(school)
			logs.append([abbrev, name, password])
		db.session.commit()
		log_file = open("logs/school_logs.csv", 'w')
		writer = csv.writer(log_file)
		writer.writerows(logs)

def populate_venues():
	logs = []
	with open('source-csvs/venues.csv') as f:
		reader = csv.reader(f, delimiter=',')
		count = 0
		for name in reader:
			logs.append(name)
			if count == 0:
				count += 1
				continue
			venue = Venue(name=name[0])
			db.session.add(venue)
		db.session.commit()
		log_file = open("logs/venues_logs.csv", 'w')
		writer = csv.writer(log_file)
		writer.writerows(logs)
		
def populate_events():
	logs = []
	with open('source-csvs/events.csv') as f:
		reader = csv.reader(f, delimiter=',')
		count = 0
		for name, description, venue, timings in reader:
			logs.append([name, description, venue, timings])
			if count == 0:
				count += 1
				continue
			event = Event(name=name,
					 description=description,
					 venue=venue,
					 timings=timings)
			db.session.add(event)
		db.session.commit()
		log_file = open("logs/events_logs.csv", 'w')
		writer = csv.writer(log_file)
		writer.writerows(logs)


def main():
	db.create_all()
	populate_venues()
	populate_schools()
	populate_events()


if __name__ == "__main__":
    	with app.app_context():
        	main()
