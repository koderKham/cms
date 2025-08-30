from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from flask_session import Session
from datetime import datetime, timedelta
import os
from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
session = Session()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configure session
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['SESSION_FILE_DIR'] = os.path.join(app.instance_path, 'sessions')
    app.config['SESSION_USE_SIGNER'] = True

    # Ensure instance and session directories exist
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    session.init_app(app)
    CORS(app)

    # Template context processor for current date/time
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    #theme loader
    @app.context_processor
    def inject_user_settings():
        # Replace this with actual database or session data
        user_settings = {
            'theme': {'mode': 'light'},
            'profile': {'name': 'John Doe', 'email': 'john.doe@example.com'},
            # Add more settings as needed
        }
        return dict(user_settings=user_settings)

    # Register blueprints

    # Add this to your create_app function where other blueprints are registered
    from app.routes.clients import clients as clients_bp
    app.register_blueprint(clients_bp, url_prefix='/clients')

    from app.routes.auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.routes.main import main as main_bp
    app.register_blueprint(main_bp)

    # Add this to your create_app function where other blueprints are registered
    from app.routes.cases import cases as cases_bp
    app.register_blueprint(cases_bp, url_prefix='/cases')

    from app.routes.people import people as people_bp
    app.register_blueprint(people_bp, url_prefix='/people')

    from app.routes.calendar import calendar_bp
    app.register_blueprint(calendar_bp, url_prefix='/calendar')

    from app.routes.notes import notes_bp
    app.register_blueprint(notes_bp, url_prefix='/notes')

    from app.routes.documents import documents_bp
    app.register_blueprint(documents_bp, url_prefix='/documents')

    from app.routes.billing import billing_bp
    app.register_blueprint(billing_bp, url_prefix='/billing')

    from app.routes.settings import settings_bp
    app.register_blueprint(settings_bp, url_prefix='/settings')

    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # Initialize database tables within the app context
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.error(f"Error creating database tables: {e}")

    return app

