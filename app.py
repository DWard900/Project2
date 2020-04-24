from flask import Flask

app = Flask(__name__)

#Change to app.py
@app.route('/')
def index():
    return "Hello World"