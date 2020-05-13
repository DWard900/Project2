import os
#Chap 4 of mega tutorial
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #WTForms needs a secret key (chap 3 of mega tutorial)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    #Chap 4 of mega tutorial
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Chap 9 of Mega Tutorial
    POSTS_PER_PAGE = 25