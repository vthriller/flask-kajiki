
from flask import Flask
from flask_kajiki import Kajiki

def create_app():
    app = Flask(__name__)

    kajiki = Kajiki(app)

    return app
