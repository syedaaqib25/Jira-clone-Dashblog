from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

# Import db from the app module to avoid circular imports
def get_db():
    return current_app.db

class User:
    def __init__(self, id=None, name=None, email=None, password_hash=None, role=None):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def from_dict(data):
        """Create User object from dictionary data"""
        return User(
            id=data.get('id'),
            name=data.get('name'),
            email=data.get('email'),
            password_hash=data.get('password_hash'),
            role=data.get('role')
        )

# --- CRUD functions ---

def create_user(name, email, password, role):
    db = get_db()
    hashed = generate_password_hash(password)
    
    # Using raw SQL for now to maintain compatibility
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute(
            'INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s) RETURNING id',
            (name, email, hashed, role)
        )
        user_id = cursor.fetchone()[0]
        db.engine.raw_connection().commit()
        return user_id
    finally:
        cursor.close()

def get_user_by_email(email):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('SELECT id, name, email, password_hash, role FROM users WHERE email = %s', (email,))
        row = cursor.fetchone()
        if row:
            # Convert to User object
            user_data = {
                'id': row[0],
                'name': row[1], 
                'email': row[2],
                'password_hash': row[3],
                'role': row[4]
            }
            return User.from_dict(user_data)
        return None
    finally:
        cursor.close()

def get_user_by_id(user_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('SELECT id, name, email, password_hash, role FROM users WHERE id = %s', (user_id,))
        row = cursor.fetchone()
        if row:
            user_data = {
                'id': row[0],
                'name': row[1],
                'email': row[2], 
                'password_hash': row[3],
                'role': row[4]
            }
            return User.from_dict(user_data)
        return None
    finally:
        cursor.close()

def check_password(stored_hash, password):
    return check_password_hash(stored_hash, password)

def get_all_users():
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('SELECT id, name FROM users')
        rows = cursor.fetchall()
        return [{'id': row[0], 'name': row[1]} for row in rows]
    finally:
        cursor.close()

def update_user_role(user_id, new_role):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('UPDATE users SET role = %s WHERE id = %s', (new_role, user_id))
        db.engine.raw_connection().commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
