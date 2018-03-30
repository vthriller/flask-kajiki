
from flask import Flask
from flask_kajiki import Genshi

def create_app():
    app = Flask(__name__)

    genshi = Genshi(app)

    return app
