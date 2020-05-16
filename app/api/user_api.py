from app import app, db
from app.models import User, Exercise
from app.api.errors import bad_request, error_response
from flask import jsonify, url_for, request, g, abort
#from app.api.auth import token_auth

@app.route('/api/users/<int:id>', methods=['GET'])
#token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())
'''
@app.route('/api/users', methods=['POST'])
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

@app.route('/api/users/<int:id>/exercise', methods=['GET'])
def get_exercise(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(user.exercise, page, per_page, get_exercise, id=id)
    return jsonify(data)