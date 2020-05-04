from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
# Chap 4 of tutorial
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes
# Chap 4 of tutorial - models will define structure of database
from app import models 