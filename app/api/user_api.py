from app import app, db
from app.models import User, Exercise
from app.api.errors import bad_request, error_response
from flask import jsonify, url_for, request, g, abort
#from app.api.auth import token_auth

@app.route('/api/users/<int:id>', methods=['GET'])
#token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())

@app.route('/api/users/<int:userId>/exercise', methods=['GET'])
def get_exercise(userId):
    user = User.query.get_or_404(userId)
    exerciseList = user.exercise.all()
    exercise = []
    for e in exerciseList:
        exercise.append({'id': e.id, 'style': e.style, 'time': e.time,
                        'timestamp': e.timestamp.isoformat() + 'Z'})
    return jsonify(exercise)

@app.route('/api/users', methods=['GET', 'POST'])
def get_user_list():
    userList = User.query.all()
    users = []
    for u in userList:
        users.append({'id': u.id, 'username': u.username, 'about_me': u.about_me,
                    'last_seen': u.last_seen.isoformat() + 'Z', 'exercise_count': u.exercise.count()})
    return jsonify(users)

@app.route('/api/users/<int:userId>/exercise/time_graph', methods=['GET'])
def exercise_graph(userId):
    user = User.query.get_or_404(userId)
    exerciseList = user.exercise.all()
    exercise = []
    for e in exerciseList:
        exercise.append({'id': e.id, 'style': e.style, 'time': e.time,})
    return jsonify(exercise)

'''@app.route('/api/users', methods=['POST'])
def register_user():
    data = request.get_json() or {}
    if 'id' not in data:
        return bad_request('Must include id')
    user = User.query.get(data['id'])
    if user is None:
        return bad_request('Unknown user')
    if user.password_hash is not None:
        return bad_request('User already registered')
    user.from_dict(data)
    db.session.commit()
    response =jsonify(user.to_dict())
    response.status_code = 201 #creating a new resource should chare the location....
    response.headers['Location'] = url_for('get_user',id=user.id)
    return response'''

'''@app.route('/api/users/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user is None:
        return bad_request('Unknown user')
    db.session.delete(user)
    db.session.commit()
    return jsonify(user.to_dict())'''