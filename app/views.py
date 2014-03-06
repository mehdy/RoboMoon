from flask import render_template, redirect, url_for, request
from app import app

@app.route('/')
@app.route('/index/')
def index():
	return render_template('index.html')

@app.route('/news/')
def news():
	return render_template('news.html')

@app.route('/sessions/')
def sessions():
	return render_template('sessions.html')

@app.route('/codes/')
def codes():
	return render_template('codes.html')

@app.route('/about/')
def about():
	return render_template('about.html')