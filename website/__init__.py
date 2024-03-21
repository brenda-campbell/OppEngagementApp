import os
from flask import Flask

def construct_app(test_config=None):
    application = Flask(__name__, instance_relative_config=True)
    application.config.from_mapping(
        SECRET_KEY='development',
        DATABASE=os.path.join(application.instance_path, 'opportunity_tracker.sqlite'),
    )

    if test_config is None:
        # Load the default configuration if it exists, unless testing
        application.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test configuration if provided
        application.config.from_mapping(test_config)

    # Make sure the instance folder is available
    try:
        os.makedirs(application.instance_path)
    except OSError:
        pass
    
    from . import models
    models.init_app(application)

    @application.route('/welcome')
    def welcome():
        return 'Welcome to the Opportunity Tracker Dashboard!'

    return application