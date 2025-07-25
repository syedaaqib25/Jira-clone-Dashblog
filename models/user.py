# NOTE: Import the shared SQLAlchemy instance that is
# initialised in models/__init__.py and bound to the Flask
# application within app.py. This prevents multiple, un-bound
# database instances and circular import issues.

from werkzeug.security import generate_password_hash, check_password_hash

from models import db

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


def create_user(name: str, email: str, password: str, role: str):
    """Create a new user and return its primary-key id."""
    hashed = generate_password_hash(password)
    user = User(name=name, email=email, password_hash=hashed, role=role)
    db.session.add(user)
    db.session.commit()
    return user.id


def _as_dict(user_obj):
    """Internal helper to convert a User model instance into a plain dict."""
    if not user_obj:
        return None
    return {
        'id': user_obj.id,
        'name': user_obj.name,
        'email': user_obj.email,
        'password_hash': user_obj.password_hash,
        'role': user_obj.role,
    }


def get_user_by_email(email: str):
    user_obj = User.query.filter_by(email=email).first()
    return _as_dict(user_obj)


def get_user_by_id(user_id):
    user_obj = User.query.get(user_id)
    return _as_dict(user_obj)


def check_password(stored_hash: str, password: str):
    """Proxy to werkzeug.security.check_password_hash for convenience."""
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
