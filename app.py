from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)



@app.route('/')
def base():
	return redirect(url_for("home"))

@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/login')
def login():
	return render_template('login.html')