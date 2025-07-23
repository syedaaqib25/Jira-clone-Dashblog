import os
from datetime import timedelta

class Config:
    # Flask secrets
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-jwt-secret-key')

    # Use DATABASE_URL from env if available, fallback to direct Render URI
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://jira_clone_db_user:OKdnwVe8v6SWtqCPKTSjZ0lkRdZYLMWJ@dpg-d1vku07gi27c738clt1g-a.oregon-postgres.render.com/jira_clone_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File upload configs (optional)
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # JWT tokens
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
