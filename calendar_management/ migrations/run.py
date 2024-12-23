from flask import Flask

def create_app(config_name):
    app = Flask(__name__)
    
    # Load the configuration based on the config_name
    app.config.from_object(config_name)
    
    # Add any other initialization, like registering blueprints, etc.
    
    return app
