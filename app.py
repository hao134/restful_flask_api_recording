import os
import secrets

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

from db import db
from blocklist import BLOCKLIST
import models

from resources.item import blp as ItemBlueprint
from resources.tag import blp as TagBlueprint
from resources.store import blp as StoreBlueprint
from resources.user import blp as UserBlueprint



def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    migrate = Migrate(app, db)
    api = Api(app)

    #secrets.SystemRandom().getrandbits(128) generates a random key as token and it will change the secret key everytime the app is restarted.
    #For that to not happen, go to the terminal, type 'python' press ENTER, type 'import secrets' press enter then type 'secrets.SystemRandom().getrandbits(128)' and press enter once again
    #The key that is generated after the terminal session will be the JWT_SECRET_KEY used
    #app.config["JWT_SECRET_KEY"] = "285856691054457386650616929138056476474"
    app.config["JWT_SECRET_KEY"] = "azeezat"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (jsonify({"description": "The token has been revoked", "error": "token_revoked"}), 401)

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (jsonify({"description": "The token is not fresh", "error": "fresh_token_required"}), 401)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (jsonify({"message": "The token has expired", "error": "Token expired"}), 401)

    @jwt.expired_token_loader
    def invalid_token_callback(error):
        return (jsonify({"message": "Signature verification failed", "error": "Invalid token"}), 401)

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (jsonify({"description": "Request does not contain an access token", "error": "Authorization required"}), 401)


    #with app.app_context():
     #   db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(UserBlueprint)
    
    return app