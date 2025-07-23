import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-jwt-secret-key')
    
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://jira_clone_db_user:OKdnwVe8v6SWtqCPKTSjZ0lkRdZYLMWJ@dpg-d1vku07gi27c738clt1g-a.oregon-postgres.render.com/jira_clone_db'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
