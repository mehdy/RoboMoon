from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, AddSessionForm, AddNewsForm, EditProfileForm, AddUserForm
from flask import render_template, redirect, url_for, request, g
from models import User, Session, News
from datetime import datetime
from app import app, db, lm
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
	if id is int:
		news = News.query.get(int(id))
		user = User.query.get(news.user_id)
		return render_template('news.html', allnews = allnews, news = news, user = user, title = 'news', ne = 'active')
	return render_template('news.html', allnews = allnews, title = 'news', user = User, ne = 'active')

@app.route('/sessions/')
@app.route('/sessions/<id>/')
def sessions(id = None):
	sessions = Session.query.all()
	sessions.reverse()
	if id:
		ss = Session.query.get(int(id))
		user = User.query.get(ss.user_id)
		return render_template('sessions.html', sessions = sessions, ss = ss, user = user, title = 'sessions', se = 'active')
	return render_template('sessions.html', sessions = sessions, title = 'sessions', user = User, se = 'active')

@app.route('/codes/')
def codes():
	return render_template('codes.html', title = 'codes', co = 'active')

@app.route('/about/')
@app.route('/about/<username>/')
def about(username = None):
	user = User.query.filter_by(username = username).first()
	users = User.query.all()
	return render_template('about.html', title = 'about',users = users, user = user, ab = 'active')

#=====================Admin section========================#
@app.route('/admin/')
@login_required
def admin():
	return render_template('admin.html', title = 'Dashboard', da = 'active')

@app.route('/admin/sessions/', methods = ['GET', 'POST'])
@app.route('/admin/sessions/<id>', methods = ['GET', 'POST'])
@login_required
def admin_sessions(id = None):
	if request.method == 'POST' and id and not request.form.values():
		db.session.delete(Session.query.get(int(id)))
		db.session.commit()
		return redirect('/admin/sessions/')
	form = AddSessionForm(request.form)
	if request.method == 'GET' and id:
		session = Session.query.get(int(id))
		form.title.data = session.title
		form.description.data = session.description
	if request.method == 'POST' and id and form.validate_on_submit():
		session = Session.query.get(int(id))
		session.title = form.title.data
		session.description = form.description.data
		session.user_id = g.user.id
		session.modified = datetime.now()
		db.session.add(session)
		db.session.commit()
	if not id and form.validate_on_submit():
		session = Session(
			title = form.title.data,
			description = form.description.data,
			user_id = g.user.id,
			modified = datetime.now())
		db.session.add(session)
		db.session.commit()
	sessions = Session.query.all()
	return render_template('admin_sessions.html', form = form, sessions = sessions, id = id, title = 'Sessions Records', se = 'active')

@app.route('/admin/news/', methods = ['GET', 'POST'])
@app.route('/admin/news/<id>', methods = ['GET', 'POST'])
@login_required
def admin_news(id = None):
	if request.method == 'POST' and id and not request.form.values():
		db.session.delete(News.query.get(int(id)))
		db.session.commit()
		return redirect('/admin/news/')
	form = AddNewsForm(request.form)
	if request.method == 'GET' and id:
		news = News.query.get(int(id))
		form.title.data = news.title
		form.description.data = news.description
	if request.method == 'POST' and id and form.validate_on_submit():
		news = News.query.get(int(id))
		news.title = form.title.data
		news.description = form.description.data
		news.user_id = g.user.id
		news.modified = datetime.now()
		db.session.add(news)
		db.session.commit()
	if not id and form.validate_on_submit():
		news = News(
			title = form.title.data,
			description = form.description.data,
			user_id = g.user.id,
			modified = datetime.now())
		db.session.add(news)
		db.session.commit()
	allnews = News.query.all()
	return render_template('admin_news.html', form = form, allnews = allnews, id = id, title = 'News', ne = 'active')

@app.route('/admin/codes/', methods = ['GET', 'POST'])
@login_required
def admin_codes():
	#Here needs to add the code section
	return render_template('admin_codes.html', title = 'codes', co = 'active')

@app.route('/admin/profile/', methods = ['GET', 'POST'])
@login_required
def admin_users():
	form = EditProfileForm(request.form)
	if request.method == 'POST':
		user = g.user
		if form.username.data:
			if not User.query.filter_by(username = form.username.data).first():
				user.username = form.username.data
		if form.email.data:
			if not User.query.filter_by(email = form.email.data).first():
				user.email = form.email.data
		if form.password.data and form.confirm.data and form.password.data == form.confirm.data:
			user.password = sha256(form.password.data).hexdigest()
		if form.website.data:
			user.website = form.website.data
		if form.bio.data:
			user.bio = form.bio.data
		db.session.add(user)
		db.session.commit()
	return render_template('admin_profile.html', form = form, user = g.user, title = 'Profile', po = 'active')

@app.route('/admin/user/', methods = ['GET', 'POST'])
@login_required
def admin_user():
	form = AddUserForm(request.form)
	if request.method == 'POST' and form.username.data and form.email.data and form.password.data and form.confirm.data and form.password.data == form.confirm.data:
		user = User(
			username = form.username.data,
			email = form.email.data,
			password = sha256(form.password.data).hexdigest())
		db.session.add(user)
		db.session.commit()
	return render_template('admin_user.html', form = form, title = 'codes', us = 'active')
