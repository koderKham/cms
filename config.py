import os
from dotenv import load_dotenv
import secrets

# Load environment variables from .env file
load_dotenv()


class Config:
    # Generate a random secret key if not set in environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)

    # Database configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              f'sqlite:///{os.path.join(basedir, "law_firm_cms.sqlite")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File upload settings
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size

    # Session settings (will be overridden in create_app)
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = True

    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')