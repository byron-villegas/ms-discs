from flask import Flask, Blueprint
from config import Config
from flask_jwt_extended import JWTManager
from flask_cors import CORS


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    jwt = JWTManager(app)

    cors = CORS(app, resources={r"/api/*": {"origins": "https://fe-discs.onrender.com"}})

    # Register blueprints here
    from app.handlers.exception_handler import bp as bp_exception_handler
    from app.discs import bp as bp_discs

    api = Blueprint("api", __name__, url_prefix=config_class.SERVER_PATH)
    api.register_blueprint(bp_discs)

    app.register_blueprint(bp_exception_handler)
    app.register_blueprint(api)

    return app