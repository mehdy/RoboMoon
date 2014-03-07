from flask import render_template, redirect, url_for, request
from app import app, db, lm
from models import User, Session, News



@app.route('/')
@app.route('/index/')
def index():
	return render_template('index.html')

@app.route('/news/')
@app.route('/news/<id>')
def news(id = None):
	allnews = News.query.all()
	allnews.reverse()
	if id:
		news = News.query.get(int(id))
		comments = Comments.query.filter_by(news_id = int(id))
		user = User.query.get(news.user_id)
		return render_template('news.html', allnews = allnews, news = news, comments = comments, user = user)
	return render_template('news.html', allnews = allnews)

@app.route('/sessions/')
@app.route('/sessions/<id>')
def sessions(id = None):
	sessions = Session.query.all()
	sessions.reverse()
	if id:
		ss = Session.query.get(int(id))
		user = User.query.get(ss.user_id)
		return render_template('sessions.html', sessions = sessions, ss = ss, user = user)
	return render_template('sessions.html', sessions = sessions)

@app.route('/codes/')
def codes():
	return render_template('codes.html')

@app.route('/about/')
def about():
	return render_template('about.html')