from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():

    #Create user data
    user = {'username': 'Elise'}

    posts = [
        {
            'author': {'username': 'Elise'},
            'body': 'Social distancing is better than people seem to believe'
        },
        {
            'author': {'username': 'Tim'},
            'body': 'Other text'
        }
    ]

    return render_template("index.html", title="Home Page", user = user, posts = posts)