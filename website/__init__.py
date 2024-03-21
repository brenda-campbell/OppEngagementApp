from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from .config import DevConfig
from .auth import auth_bp
from .base import base_bp
from .auth.models import User
import os

# Define db and migrate as global variables and initialised login manger
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()

def construct_app(test_config=None):
    # Load environment variables from .env file
    load_dotenv()
    
    application = Flask(__name__, instance_relative_config=True)
    application.config.from_mapping(
        SECRET_KEY= os.getenv('SECRET_KEY', 'development'),
        DATABASE=os.path.join(application.instance_path, 'opportunity_tracker.sqlite'),
    )
    
     # Initialize login_manager with application
    login_manager.init_app(application)

    if test_config is None:
        # Load the default configuration if it exists, unless testing
        application.config.from_object(DevConfig)  # Use DevConfig for development
    else:
        # Load the test configuration if provided
        application.config.from_mapping(test_config)

    # Make sure the instance folder is available
    try:
        os.makedirs(application.instance_path)
    except OSError:
        pass

    # Initialize db and migrate with the application
    db.init_app(application)
    migrate.init_app(application, db)
    Bcrypt(application)

    application.register_blueprint(auth_bp)
    application.register_blueprint(base_bp)

    @application.route('/welcome')
    def welcome():
        return 'Welcome to the Opportunity Tracker Dashboard!'

    return application