from flask import Flask
from app.extensions import db
from app.config import Config
from dotenv import load_dotenv
from flask_cors import CORS
import logging

load_dotenv()

def create_app():
    # Create the Flask application instance
    app = Flask(__name__)

    # Load configuration settings
    app.config.from_object(Config)

    # Enable CORS for frontend interaction
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

    # Initialize database
    db.init_app(app)

    # Import and register models
    try:
        from app.models import Admin
    except ImportError as e:
        logging.error(f"Error importing models: {e}")
        raise

    # Ensure database tables exist
    with app.app_context():
        try:
            db.create_all()
            logging.info("Database tables created successfully.")
        except Exception as e:
            logging.error(f"Error creating database tables: {e}")
            raise

    # Register blueprints for routes
    try:
        from app.routes import register_blueprints
        register_blueprints(app)
        logging.info("Blueprints registered successfully.")
    except ImportError as e:
        logging.error(f"Error importing routes: {e}")
        raise
    except Exception as e:
        logging.error(f"Error registering blueprints: {e}")
        raise

    # Return the Flask app instance
    return app
