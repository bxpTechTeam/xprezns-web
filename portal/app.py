from flask import Flask, render_template, request, redirect, url_for
from models import *
from flask_socketio import SocketIO
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///portal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'DBBRegSecretKey'
db.init_app(app)
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

@app.route('/login_page')
def login_page():
    schools = School.query.all()
    return render_template('login.html', schools=schools)

@login_manager.user_loader
def load_user(user_id):
    return School.query.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('registration'))
    # Add Javascript to display problems
    if request.method == 'GET':
        return redirect(url_for('login_page'))
    uname = request.form.get('username')
    password = request.form.get('password')
    if sha512(password.encode('utf-8')).hexdigest() == School.query.get(uname).passwd:
        print("Login successful")
        login_user(load_user(uname))
        return redirect(url_for('registration'))
    else:
        print("Wrong Password")
        failed = True
        return redirect(url_for('login_page'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('/'))

@app.route('/registration')
@login_required
def registration():
    print(current_user.abbrev)
    events = Event.query.all()
    registered = EventRegistrationEntry.query.filter_by(school_name = current_user.abbrev)
    for row in registered:
        events.remove(Event.query.get(row.event_name))
    return render_template('register.html', events=events)

@socketio.on("register")
@login_required
def register(data):
    event = data['event']
    print(f'{current_user.abbrev} : {event}')
    db.session.add(EventRegistrationEntry(event_name=event,school_name=current_user.abbrev))
    db.session.commit()


############# ERROR HANDLERS ###############
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404
