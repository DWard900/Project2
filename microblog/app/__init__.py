from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
# Chap 4 of tutorial
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Chap 5 of tutorial
login = LoginManager(app)
login.login_view = 'login'

from app import routes
# Chap 4 of tutorial - models will define structure of database
from app import models 