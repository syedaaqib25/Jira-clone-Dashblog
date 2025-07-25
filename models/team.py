from flask import current_app

def get_db():
    return current_app.db

def create_team(name, project_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute(
            'INSERT INTO teams (name, project_id) VALUES (%s, %s) RETURNING id',
            (name, project_id)
        )
        team_id = cursor.fetchone()[0]
        db.engine.raw_connection().commit()
        return team_id
    finally:
        cursor.close()

def get_teams_by_project(project_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('SELECT * FROM teams WHERE project_id = %s', (project_id,))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    finally:
        cursor.close()

def assign_team_to_project(team_id, project_id):
    # This functionality might be handled by the create_team function
    # or through project_users table for team membership
    pass

def get_team_by_id(team_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('SELECT * FROM teams WHERE id = %s', (team_id,))
        row = cursor.fetchone()
        if row:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
        return None
    finally:
        cursor.close() 