from flask import Flask
from config import Config

# import our blueprints
from .auth.routes import auth
from .ig.routes import ig

# import our db related
from .models import db
from flask_migrate import Migrate

app  = Flask(__name__)

app.register_blueprint(auth)
app.register_blueprint(ig)

app.config.from_object(Config)

# initialize our database to work with our app
db.init_app(app)

migrate = Migrate(app, db)

from . import routes
from . import models