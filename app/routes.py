from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, AdminRegistrationForm , EditProfileForm, ExerciseForm, EmptyForm, SetGoal, MessageForm 
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Exercise, Message
from werkzeug.urls import url_parse
from datetime import datetime
from app.api.auth import token_auth, basic_auth

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    exercise = current_user.followed_posts().all()

    return render_template("index.html", title="Home", exercise = exercise, user=user)

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

# Results page after quiz is posted
@app.route('/results')
@login_required
def results():
    return render_template("results.html", title="Results Page")

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    form = ExerciseForm()
    if form.validate_on_submit():
        style = form.style.data
        time = form.time.data
        exercise_date = form.date.data
        distance = form.distance.data
        mins_per_k = round(form.time.data / form.distance.data, 2)
        rating=form.rate_exercise.data
        comment=form.exercise_comments.data
        exercise = Exercise(style=form.style.data, time=form.time.data, exercise_date=form.date.data, distance=form.distance.data, 
        rate_exercise=form.rate_exercise.data, exercise_comments=form.exercise_comments.data, user=current_user)
        db.session.add(exercise)
        db.session.commit()
        return render_template("results.html", title="Results Page", style=style, time=time, 
        exercise_date=exercise_date, distance=distance, mins_per_k=mins_per_k, rating=rating, comment=comment, user=user)
    return render_template("quiz.html", title="Quiz Page", form=form, user=user)

# Group view page
@app.route('/groupview')
@login_required
def groupview():
    return render_template("groupview.html", title="Group View")

# All users page
@app.route('/users_page')
@login_required
def users_page():
    users = User.query.all()
    followed_posts = current_user.followed_posts().all()
    return render_template("userview.html", title="All Users", users=users, followed_posts=followed_posts)

# User profile
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    exercises = Exercise.query.filter_by(user_id=user.id)
    form = EmptyForm()
    return render_template('user.html', user=user, exercises=exercises, form=form)

# Follow a user
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

# Unfollow a user
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

# Edit profile button on user page
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

# Set/change goal
@app.route('/set_goal/<username>', methods=['GET', 'POST'])
@login_required
def set_goal(username):
   form = SetGoal()
   if form.validate_on_submit():
       user = User.query.filter_by(username=username).first()
       user.goals = form.goals.data
       db.session.commit()
       flash('Your changes have been saved.')
       return redirect(url_for('index'))
   return render_template('set_goal.html', title='set goal', form=form)

# Admin login screen
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        password = form.password.data
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        if user.is_admin == False:
            flash('Not an admin user')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        return render_template('adminview.html', username=user, password=password)
    return render_template('admin_sign_in.html', title='Admin Sign In', form=form)

# Delete post
@app.route('/delete_post/<int:exercise_id>', methods= ['POST'])
@login_required
def delete_post(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    db.session.delete(exercise)
    db.session.commit()
    flash('Entry was deleted')
    return redirect(url_for('user', username=current_user.username))

# Send message to user
@app.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('user', username=recipient))
    return render_template('send_message.html', title=('Send Message'),
                           form=form, recipient=recipient)

# See all messages
@app.route('/messages/<username>')
@login_required
def messages(username):
    user = User.query.filter_by(username=username).first_or_404()
    messages = Message.query.filter_by(recipient_id=user.id)
    form = EmptyForm()
    return render_template('messages.html', messages=messages, form=form)

# Delete message
@app.route('/delete_message/<int:message_id>', methods= ['POST'])
@login_required
def delete_message(message_id):
    message = Message.query.get(message_id)
    db.session.delete(message)
    db.session.commit()
    flash('Message was deleted')
    return redirect(url_for('messages', username=current_user.username))

# Add a user on admin view
@app.route('/admin_login/add_user', methods=['GET', 'POST'])
def add_user():
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        
        user = User(username=form.username.data, email=form.email.data, is_admin=form.admin.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('add_user.html', title='Register', form=form)

# Delete a user on admin view
@app.route('/admin_login/delete_user')
@login_required
def admin_delete_user():
    users = User.query.all()
    return render_template("delete_users.html", title="delete_user", users = users)

@app.route('/delete_user/<username>', methods= ['GET', 'POST'])
@login_required
def delete_user(username):
    users = User.query.all()
    user = User.query.filter_by(username=username).first_or_404()
    db.session.delete(user)
    db.session.commit()
    users = User.query.all()
    flash('User was deleted')
    return redirect(url_for('admin_delete_user', title="delete_user", users=users))


