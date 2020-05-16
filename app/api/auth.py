'''from flask import g
from flask_httpauth import HTTPBasicAuth
from app.models import User
from app.api.errors import error_response
from flask_httpauth import HTTPTokenAuth

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

#password required for granting tokens 
@basic_auth.verify_password
def verify_password(id, password):
  user = User.query.get(id)
  if user is None:
    return False
  g.current_user = user
  return user.check_password_hash(password)

@basic_auth.error_handler
def basic_auth_error():
  return error_response(401)

#token auth below
@token_auth.verify_token
def verify_token(token):
  g.current_user = User.check_token(token) if token else None
  return g.current_user is not None

@token_auth.error_handler
def token_auth_error():
  return error_response(401)'''