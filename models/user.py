from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb.cursors

def create_user(name, email, password, role):
    cursor = current_app.mysql.connection.cursor()
    password_hash = generate_password_hash(password)
    cursor.execute('INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)', (name, email, password_hash, role))
    current_app.mysql.connection.commit()
    return cursor.lastrowid

def get_user_by_email(email):
    cursor = current_app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    return cursor.fetchone()

def get_user_by_id(user_id):
    cur = current_app.mysql.connection.cursor()
    cur.execute("SELECT id, name FROM users WHERE id=%s", (user_id,))
    row = cur.fetchone()
    cur.close()
    if row:
        return {'id': row[0], 'name': row[1]}
    return None

def check_password(stored_hash, password):
    return check_password_hash(stored_hash, password)

def get_all_users():
    cur = current_app.mysql.connection.cursor()
    cur.execute("SELECT id, name FROM users")
    rows = cur.fetchall()
    cur.close()
    return [{'id': row[0], 'name': row[1]} for row in rows]

def update_user_role(user_id, new_role):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute('UPDATE users SET role = %s WHERE id = %s', (new_role, user_id))
    current_app.mysql.connection.commit() 