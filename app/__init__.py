from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



# Instances of packages
login = LoginManager()
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Initializing section
    app = Flask(__name__)

    #link to our conifg
    app.config.from_object(Config)
    
    # Register Packages
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Configure login settings
    login.login_view = 'auth.login'
    login.login_message = 'You have to login first'
    login.login_message_category = 'warning'

    #Importing blueprints
    from app.blueprints.main import main 
    from app.blueprints.auth import auth
    #Registering blueprints

    app.register_blueprint(main)
    app.register_blueprint(auth)
    return app