from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from models.forms import SignUpForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'QLIA1cy9Svg4lgai'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tweetplane.db'
""" app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True # use false for production """

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
from models.user import User

""" @app.before_first_request
def setup():
    db.Model.metadata.drop_all(bind=db.engine)
    db.Model.metadata.create_all(bind=db.engine)
# When the Flask app is shutting down, close the database session
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove() """


@app.route('/')
def base():
	return redirect(url_for("home"))

@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash(f'Welcome back {form.username.data}!', 'success')
		return redirect(url_for('home'))
	return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignUpForm()
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('home'))
	return render_template('signup.html', form=form)