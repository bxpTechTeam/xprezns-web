from flask import Flask, render_template, request, redirect, url_for
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///portal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


username = ""
is_logged_in = False
failed=False

@app.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

@app.route('/login_page')
def login_page():
	schools = School.query.all()
	if failed:
		return render_template('login.html', schools=schools)
	return render_template('login.html', schools=schools)
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return redirect(url_for('login_page'))
	uname = request.form.get('username')
	password = request.form.get('password')
	if sha512(password.encode('utf-8')).hexdigest() == School.query.get(uname).passwd:
		print("Login successful")
		is_logged_in = True
		username = uname
		failed = False
		return redirect(url_for('login_page'))
	else:
		print("Wrong Password")
		failed = True
		return redirect(url_for('login_page'))
	
	

############# ERROR HANDLERS ###############
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404