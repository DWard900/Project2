from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ExerciseForm, EmptyForm, SetGoal
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Exercise
from werkzeug.urls import url_parse
from datetime import datetime
from app.api.auth import token_auth, basic_auth

@app.route('/')
@app.route('/index')
@login_required
def index():
    #Create user data
    exercise = current_user.followed_posts().all()

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
    exercises = Exercise.query.filter_by(user_id=user.id)
    form = EmptyForm()
    return render_template('user.html', user=user ,exercises=exercises , form=form)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

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

@app.route('/set_goal/<username>', methods=['GET', 'POST'])
@login_required
def set_goal(username):
   form = SetGoal()
   if form.validate_on_submit():
       user = User.query.filter_by(username=username).first()
       user.goals = form.goals.data
       db.session.commit()
       flash('Your changes have been saved.')
       return redirect(url_for('set_goal'))
   return render_template('set_goal.html', title='set goal', form=form)

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    form = ExerciseForm()
    if form.validate_on_submit():
        exercise = Exercise(style=form.style.data, time=form.time.data, distance=form.distance.data, user=current_user)
        db.session.add(exercise)
        db.session.commit()
        flash('Thank you for submitting')
        return redirect(url_for('index'))

    return render_template("quiz.html", title="Quiz Page", form=form)

@app.route('/admin/<username>')
def admin(username, password):
    return render_template('adminview.html', username=username, password=password)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        password = form.password.data
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        #next_page = request.args.get('next')
        #if not next_page or url_parse(next_page).netloc != '':
        #    next_page = url_for('admin')
        return admin(user, password)
    return render_template('admin_sign_in.html', title='Admin Sign In', form=form)

#delete post
@app.route('/delete_post/<int:exercise_id>', methods= ['POST'])
@login_required
def delete_post(exercise_id):
    #db.session.execute('delete from Exercise WHERE id = %s', [id])
    exercise = Exercise.query.get(exercise_id)
    db.session.delete(exercise)
    db.session.commit()
    flash('Entry was deleted')
    return redirect('http://127.0.0.1:5000/user/ward')