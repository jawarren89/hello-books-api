from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# conventional variables that give us access to db and migrate operations
db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)

    # hides a warning about a feature we won't be using
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # sets configuration to connection string in order to connect database
    if not test_config:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    else:
        # app.config["TESTING"] = True      # Turns testing on
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")

    #register model for Book (and any others) with app startup
    from app.models.book import Book
    from app.models.author import Author

    # db and migrate are initialized with app startup
    db.init_app(app)
    migrate.init_app(app, db)

    # register Blueprints here with app startup
    from .routes import books_bp
    app.register_blueprint(books_bp)
    # app.register_blueprint(hello_world_bp)

    return app