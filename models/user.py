from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# --- CRUD functions ---

def create_user(name, email, password, role):
    hashed = generate_password_hash(password)
    user = User(name=name, email=email, password_hash=hashed, role=role)
    db.session.add(user)
    db.session.commit()
    return user.id

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def check_password(stored_hash, password):
    return check_password_hash(stored_hash, password)

def get_all_users():
    users = User.query.all()
    return [{'id': u.id, 'name': u.name} for u in users]

def update_user_role(user_id, new_role):
    user = User.query.get(user_id)
    if user:
        user.role = new_role
        db.session.commit()
        return True
    return False
