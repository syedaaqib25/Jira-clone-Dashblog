from flask import current_app as app
import MySQLdb.cursors

def create_project(name, description, priority, created_by):
    cursor = app.mysql.connection.cursor()
    cursor.execute(
        'INSERT INTO projects (name, description, priority, created_by) VALUES (%s, %s, %s, %s)',
        (name, description, priority, created_by)
    )
    app.mysql.connection.commit()
    return cursor.lastrowid

def get_project_by_id(project_id):
    cursor = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM projects WHERE id = %s', (project_id,))
    return cursor.fetchone()

def get_all_projects():
    cursor = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM projects')
    return cursor.fetchall()

def update_project(project_id, name, description, priority):
    cursor = app.mysql.connection.cursor()
    cursor.execute('UPDATE projects SET name = %s, description = %s, priority = %s WHERE id = %s', (name, description, priority, project_id))
    app.mysql.connection.commit()

def delete_project(project_id):
    cursor = app.mysql.connection.cursor()
    cursor.execute('DELETE FROM projects WHERE id = %s', (project_id,))
    app.mysql.connection.commit()
