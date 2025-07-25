from flask_sqlalchemy import SQLAlchemy

# Shared SQLAlchemy instance for the entire application
# It will be initialised with the Flask app inside app.py

# Expose a single db object that other modules can import:
db = SQLAlchemy() 