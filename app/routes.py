from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm,RedditForm
from app.models import User
import praw

@app.route('/')
@app.route('/index')
@login_required
def index():
    
    return render_template('index.html', title='Home')


        


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/reddit',methods=['GET','POST'])
def reddit():
	if current_user.is_authenticated:
		form = RedditForm()
		#print("IS")
		if form.validate_on_submit():
			#print("IN")
			sub= request.form['sub']
			reddit=praw.Reddit(client_id = 'f3G0avzj-27sXA', client_secret= 'iYK7z9qylnyGKUgx0eAviIRBOCI', username = 'sosio_app', password = 'Sosio@123', user_agent ='sosio_app')
			subreddit=reddit.subreddit(sub)
			popular=subreddit.hot()
			return render_template('redditdata.html',title='Reddit Data',popular=popular)	      
	
			
		return render_template('reddit.html',title="Reddit",form=form)		
