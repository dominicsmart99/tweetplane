from flask import render_template, redirect, url_for, flash, request
from tweetplane import app, db, bcrypt
from tweetplane.models.forms import SignUpForm, LoginForm
from tweetplane.models.user import User
from flask_login import login_user, logout_user, current_user, login_required

@app.before_first_request
def setup():
    db.Model.metadata.drop_all(bind=db.engine)
    db.Model.metadata.create_all(bind=db.engine)
# When the Flask app is shutting down, close the database session
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


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
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome back {form.username.data}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else: flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/account')
@login_required
def account():
    return render_template('account.html')