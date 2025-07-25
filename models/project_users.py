from flask import current_app

def get_db():
    return current_app.db

def add_project_user(user_id, project_id, role):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute(
            'INSERT INTO project_users (user_id, project_id, role) VALUES (%s, %s, %s) RETURNING id', 
            (user_id, project_id, role)
        )
        project_user_id = cursor.fetchone()[0]
        db.engine.raw_connection().commit()
        return project_user_id
    finally:
        cursor.close()

def get_users_by_project(project_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute(
            'SELECT pu.*, u.name, u.email FROM project_users pu JOIN users u ON pu.user_id = u.id WHERE pu.project_id = %s', 
            (project_id,)
        )
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    finally:
        cursor.close()

def update_project_user_role(user_id, project_id, role):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute(
            'UPDATE project_users SET role = %s WHERE user_id = %s AND project_id = %s', 
            (role, user_id, project_id)
        )
        db.engine.raw_connection().commit()
    finally:
        cursor.close()

def remove_project_user(user_id, project_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('DELETE FROM project_users WHERE user_id = %s AND project_id = %s', (user_id, project_id))
        db.engine.raw_connection().commit()
    finally:
        cursor.close() 