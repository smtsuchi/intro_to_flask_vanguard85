from flask import Flask
from config import Config

# import our blueprints
from .auth.routes import auth

app  = Flask(__name__)

app.register_blueprint(auth)

app.config.from_object(Config)

from . import routes