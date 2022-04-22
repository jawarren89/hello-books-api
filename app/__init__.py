from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

# db = SQLAlchemy
# migrate = Migrate

def create_app(test_config=None):
    app = Flask(__name__)

    #register Blueprints here
    from .routes import hello_world_bp, books_bp
    app.register_blueprint(hello_world_bp)
    app.register_blueprint(books_bp)

    return app