from flask import current_app

def get_db():
    return current_app.db

def create_sprint(name, project_id, start_date, end_date, status='Active'):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute(
            'INSERT INTO sprints (name, project_id, start_date, end_date, status) VALUES (%s, %s, %s, %s, %s) RETURNING id',
            (name, project_id, start_date, end_date, status)
        )
        sprint_id = cursor.fetchone()[0]
        db.engine.raw_connection().commit()
        return sprint_id
    finally:
        cursor.close()

def get_sprints_by_project(project_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('SELECT * FROM sprints WHERE project_id = %s', (project_id,))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    finally:
        cursor.close()

def get_sprint_by_id(sprint_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('SELECT * FROM sprints WHERE id = %s', (sprint_id,))
        row = cursor.fetchone()
        if row:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
        return None
    finally:
        cursor.close()

def update_sprint(sprint_id, name, start_date, end_date, status):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute(
            'UPDATE sprints SET name = %s, start_date = %s, end_date = %s, status = %s WHERE id = %s',
            (name, start_date, end_date, status, sprint_id)
        )
        db.engine.raw_connection().commit()
    finally:
        cursor.close()

def delete_sprint(sprint_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('DELETE FROM sprints WHERE id = %s', (sprint_id,))
        db.engine.raw_connection().commit()
    finally:
        cursor.close()
