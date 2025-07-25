from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
# Database imports
from models import db  # Shared SQLAlchemy instance
from flask_mysqldb import MySQL
from config.config import Config
from dotenv import load_dotenv
import os

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Flask App Setup
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object(Config)

# ✅ SQLAlchemy initialisation (uses shared instance from models)
db.init_app(app)
app.db = db  # make accessible via current_app.db

# ✅ MySQL initialisation (for legacy/raw-SQL parts of the codebase)
# Default configuration values can be overridden via environment variables.
app.config.setdefault('MYSQL_HOST', os.environ.get('MYSQL_HOST', 'localhost'))
app.config.setdefault('MYSQL_PORT', int(os.environ.get('MYSQL_PORT', '3306')))
app.config.setdefault('MYSQL_USER', os.environ.get('MYSQL_USER', 'root'))
app.config.setdefault('MYSQL_PASSWORD', os.environ.get('MYSQL_PASSWORD', ''))
app.config.setdefault('MYSQL_DB', os.environ.get('MYSQL_DB', 'jira_clone'))

mysql = MySQL(app)
# Expose as attribute so models/routes can access via current_app.mysql
app.mysql = mysql

# ✅ JWT Setup
jwt = JWTManager(app)

@jwt.unauthorized_loader
def unauthorized_callback(callback):
    return jsonify({'msg': 'Missing Authorization Header'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(callback):
    return jsonify({'msg': 'Invalid token'}), 422

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'msg': 'Token has expired'}), 401

# ✅ Enable CORS
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}}, allow_headers=["Content-Type", "Authorization"])

# ✅ Register Blueprints
from routes.auth import auth_bp
from routes.projects import projects_bp
from routes.issues import issues_bp
from routes.comments import comments_bp
from routes.users import users_bp
from routes.messages import bp as messages_bp
from routes.board import board_bp
from routes.notifications import notifications_bp
from routes.sprints import sprint_bp

app.register_blueprint(auth_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(issues_bp)
app.register_blueprint(comments_bp)
app.register_blueprint(users_bp)
app.register_blueprint(messages_bp)
app.register_blueprint(board_bp)
app.register_blueprint(notifications_bp)
app.register_blueprint(sprint_bp)

# ✅ Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:path>')
def static_proxy(path):
    if os.path.exists(os.path.join('templates', path)):
        return render_template(path)
    return send_from_directory('static', path)

# ✅ Ensure upload folder exists
upload_path = os.path.join(app.root_path, 'static', 'uploads')
if not os.path.exists(upload_path):
    os.makedirs(upload_path)
    print(f"Upload folder created at: {upload_path}")
app.config['UPLOAD_FOLDER'] = upload_path

# ✅ Entry Point
if __name__ == '__main__':
    app.run(debug=True)
