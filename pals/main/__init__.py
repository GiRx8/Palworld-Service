import os
from flask import Flask
from .configurations.config import Config

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)
    # Load the default configuration from config.py
    #print(app.config)

    if not os.path.exists(Config.INSTANCE_PATH):
        os.makedirs(Config.INSTANCE_PATH)

    # Register blueprints and extensions
    from . import db
    db.init_app(app)

    from .utils import server_config
    app.register_blueprint(server_config.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from main.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from .utils.service_control import service_control_bp
    app.register_blueprint(service_control_bp)

    from .configurations.config import Configs_bp
    app.register_blueprint(Configs_bp)
    
    return app