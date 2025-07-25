from flask import current_app

def get_db():
    return current_app.db

def create_project(name, description, priority, created_by):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute(
            'INSERT INTO projects (name, description, priority, created_by) VALUES (%s, %s, %s, %s) RETURNING id',
            (name, description, priority, created_by)
        )
        project_id = cursor.fetchone()[0]
        db.engine.raw_connection().commit()
        return project_id
    finally:
        cursor.close()

def get_project_by_id(project_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('SELECT * FROM projects WHERE id = %s', (project_id,))
        row = cursor.fetchone()
        if row:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
        return None
    finally:
        cursor.close()

def get_all_projects():
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('SELECT * FROM projects')
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    finally:
        cursor.close()

def update_project(project_id, name, description, priority):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute(
            'UPDATE projects SET name = %s, description = %s, priority = %s WHERE id = %s', 
            (name, description, priority, project_id)
        )
        db.engine.raw_connection().commit()
    finally:
        cursor.close()

def delete_project(project_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('DELETE FROM projects WHERE id = %s', (project_id,))
        db.engine.raw_connection().commit()
    finally:
        cursor.close()
