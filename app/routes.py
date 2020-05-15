from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ExerciseForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Exercise
from werkzeug.urls import url_parse
from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():

    #Create user data
    user = {'username': 'Elise'}

    exercise = Exercise.query.all()

    return render_template("index.html", title="Home", exercise = exercise)

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
        return redirect(url_for('index'))
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

@app.route('/results')
@login_required
def results():
    return render_template("results.html", title="Results Page")

@app.route('/groupview')
@login_required
def groupview():
    return render_template("groupview.html", title="Group View")

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    exercise = Exercise.query.filter_by(user_id=user.id)
    return render_template('user.html', user=user, exercise=exercise)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    form = ExerciseForm()
    if form.validate_on_submit():
        exercise = Exercise(style=form.style.data, time=form.time.data, user=current_user)
        db.session.add(exercise)
        db.session.commit()
        flash('Thank you for submitting')
        return redirect(url_for('index'))

    return render_template("quiz.html", title="Quiz Page", form=form)