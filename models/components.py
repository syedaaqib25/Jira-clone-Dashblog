from flask import current_app

def get_db():
    return current_app.db

def create_component(name, description, project_id, lead_id=None):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute(
            "INSERT INTO components (name, description, project_id, lead_id) VALUES (%s, %s, %s, %s) RETURNING id", 
            (name, description, project_id, lead_id)
        )
        component_id = cursor.fetchone()[0]
        db.engine.raw_connection().commit()
        return component_id
    finally:
        cursor.close()

def get_components_by_project(project_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute("SELECT * FROM components WHERE project_id = %s", (project_id,))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    finally:
        cursor.close()

def update_component(component_id, name, description=None):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        if description is not None:
            cursor.execute(
                "UPDATE components SET name = %s, description = %s WHERE id = %s", 
                (name, description, component_id)
            )
        else:
            cursor.execute("UPDATE components SET name = %s WHERE id = %s", (name, component_id))
        db.engine.raw_connection().commit()
    finally:
        cursor.close()

def delete_component(component_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute("DELETE FROM components WHERE id = %s", (component_id,))
        db.engine.raw_connection().commit()
    finally:
        cursor.close()
