from flask.ext.login import login_user, logout_user, current_user, login_required
from flask import render_template, redirect, url_for, request, g
from models import User, Session, News
from app import app, db, lm
from forms import LoginForm
from hashlib import sha256

#================Login & Logout==================#
@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user

@app.route('/login/', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		form = LoginForm(request.form)
		user = User.query.filter_by(email = form.email.data).first()
		if user:
			if user.password == sha256(form.password.data).hexdigest():
				login_user(user, remember = form.remember_me.data)
		if g.user is not None and g.user.is_authenticated():
			return redirect(request.args.get('next') or url_for('admin'))
	return render_template('login.html')

@app.route('/logout/')
@login_required
def logout():
	logout_user()
	return redirect(request.args.get('next') or url_for('index'))

#====================Main Pages====================#

@app.route('/')
@app.route('/index/')
def index():
	return render_template('index.html', ho = 'active')

@app.route('/news/')
@app.route('/news/<id>/')
def news(id = None):
	allnews = News.query.all()
	allnews.reverse()
	if id:
		news = News.query.get(int(id))
		user = User.query.get(news.user_id)
		return render_template('news.html', allnews = allnews, news = news, comments = comments, user = user, title = 'news', ne = 'active')
	return render_template('news.html', allnews = allnews, title = 'news', ne = 'active')

@app.route('/sessions/')
@app.route('/sessions/<id>/')
def sessions(id = None):
	sessions = Session.query.all()
	sessions.reverse()
	if id:
		ss = Session.query.get(int(id))
		user = User.query.get(ss.user_id)
		return render_template('sessions.html', sessions = sessions, ss = ss, user = user, title = 'sessions', se = 'active')
	return render_template('sessions.html', sessions = sessions, title = 'sessions', se = 'active')

@app.route('/codes/')
def codes():
	return render_template('codes.html', title = 'codes', co = 'active')

@app.route('/about/')
@app.route('/about/<username>/')
def about(username = None):
	return render_template('about.html', title = 'about', ab = 'active')

#=====================Admin section========================#
@app.route('/admin/')
@login_required
def admin():
	return render_template('admin.html')

@app.route('/admin/sessions/')
@login_required
def admin_sessions():
	return render_template('admin_sessions.html')

@app.route('/admin/news/')
@login_required
def admin_news():
	return render_template('admin_news.html')

@app.route('/admin/codes/')
@login_required
def admin_codes():
	return render_template('admin_codes.html')

@app.route('/admin/users/')
@app.route('/admin/users/<username>/')
@login_required
def admin_users(username = None):
	return render_template('admin_users.html')