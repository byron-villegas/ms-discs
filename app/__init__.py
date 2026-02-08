from flask import Flask, Blueprint
from app.config import Config
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    jwt = JWTManager(app)

    cors = CORS(app, resources={r"/*": {"origins": config_class.CORS_ORIGIN}})

    # Importar modelos para generar schemas
    from app.discs.models import Disc, Track

    # Configurar Flasgger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/swagger-ui/"
    }
    
    swagger_template = {
        "info": {
            "title": "MS Discs API",
            "description": "Microservicio para gestión de colección de discos",
            "version": "1.0.0",
            "contact": {
                "name": "API Support"
            }
        },
        "servers": [
            {
                "url": f"http://127.0.0.1:{config_class.SERVER_PORT}{config_class.SERVER_PATH}",
                "description": "Servidor de desarrollo"
            }
        ],
        "tags": [
            {
                "name": "Discs",
                "description": "Operaciones relacionadas con discos"
            }
        ]
    }
    
    # Generar schemas de Pydantic
    disc_schema = Disc.model_json_schema(ref_template='#/definitions/{model}')
    track_schema = Track.model_json_schema()
    
    # Extraer definiciones anidadas si existen
    definitions = {}
    if '$defs' in disc_schema:
        definitions.update(disc_schema.pop('$defs'))
    
    definitions['Disc'] = disc_schema
    definitions['Track'] = track_schema
    definitions['BusinessError'] = {
        "type": "object",
        "properties": {
            "codigo": {
                "type": "string",
                "example": "EXDNE01"
            },
            "mensaje": {
                "type": "string",
                "example": "Disco no encontrado"
            }
        }
    }
    definitions['ValidationError'] = {
        "type": "object",
        "properties": {
            "errors": {
                "type": "array",
                "items": {
                    "type": "object"
                }
            }
        }
    }
    
    swagger_template['definitions'] = definitions
    
    Swagger(app, config=swagger_config, template=swagger_template)

    # Register blueprints here
    from app.handlers.exception_handler import bp as bp_exception_handler
    from app.discs import bp as bp_discs

    api = Blueprint("api", __name__, url_prefix=config_class.SERVER_PATH)
    
    # Health check endpoint
    @api.route('/health', methods=['GET'])
    def health_check():
        return {
            "status": "healthy",
            "service": "ms-discs",
            "version": "1.0.0"
        }, 200
    
    api.register_blueprint(bp_discs)

    app.register_blueprint(bp_exception_handler)
    app.register_blueprint(api)

    return app