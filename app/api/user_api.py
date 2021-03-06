from app import app, db
from app.models import User, Exercise
from app.api.errors import bad_request, error_response
from flask import jsonify, url_for, request, g, abort
from app.api.auth import token_auth
from flask_login import login_required

@app.route('/api/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())

# API to get user exercise
@app.route('/api/users/<int:userId>/exercise', methods=['GET'])
def get_exercise(userId):
    user = User.query.get_or_404(userId)
    exerciseList = user.exercise.all()
    exercise = []
    for e in exerciseList:
        mins_per_k = round(float(e.time) / float(e.distance), 2)
        exercise.append({'id': e.id, 'style': e.style, 'time': e.time, 'distance': e.distance,
                        'exercise_date': e.exercise_date.strftime("%A, %d %B %Y"), 
                        'speed': mins_per_k, 'rate_exercise': e.rate_exercise, 
                        'exercise_comments': e.exercise_comments})
    return jsonify(exercise)

# API to get all users
@app.route('/api/users', methods=['GET', 'POST'])
@token_auth.login_required
def get_user_list():
    userList = User.query.all()
    users = []
    for u in userList:
        users.append({'id': u.id, 'username': u.username, 'about_me': u.about_me,
                    'last_seen': u.last_seen.strftime("%A, %d %B %Y at %H:%M UTC"), 'exercise_count': u.exercise.count()})
    return jsonify(users)

# API to get exercise for one user for graphs
@app.route('/api/users/<int:userId>/exercise/graphs', methods=['GET'])
def exercise_graph(userId):
    user = User.query.get_or_404(userId)
    exerciseList = user.exercise.all()
    exercise = []
    for e in exerciseList:
        mins_per_k = round(float(e.time) / float(e.distance), 2)
        exercise.append({'id': e.id, 'style': e.style, 'time': e.time, 'distance': e.distance,
        'exercise_date': e.exercise_date.strftime("%Y-%m-%d"), 'speed': mins_per_k})
    return jsonify(exercise)

# API to get exercise for all users
@app.route('/api/users/all/exercise', methods=['GET'])
def exercise_all():
    userList = User.query.all()
    users = []
    for u in userList:
        exercises = u.exercise.all()
        for e in exercises:
            users.append({'id': u.id, 'username': u.username, 'style': e.style, 'distance':e.distance , 'time': e.time , 'date': e.exercise_date.strftime("%Y-%m-%d") })
    return jsonify(users)
