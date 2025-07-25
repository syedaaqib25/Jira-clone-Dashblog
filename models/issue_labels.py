from flask import current_app

def get_db():
    return current_app.db

def create_label(name, color, project_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute(
            'INSERT INTO issue_labels (name, color, project_id) VALUES (%s, %s, %s) RETURNING id', 
            (name, color, project_id)
        )
        label_id = cursor.fetchone()[0]
        db.engine.raw_connection().commit()
        return label_id
    finally:
        cursor.close()

def get_labels_by_project(project_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('SELECT * FROM issue_labels WHERE project_id = %s', (project_id,))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    finally:
        cursor.close()

def delete_label(label_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('DELETE FROM issue_labels WHERE id = %s', (label_id,))
        db.engine.raw_connection().commit()
    finally:
        cursor.close()

# Legacy functions for backward compatibility
def add_issue_label(issue_id, label):
    # This might need to be implemented differently based on how labels are associated with issues
    # For now, just create a label if it doesn't exist
    pass

def get_labels_by_issue(issue_id):
    # This would require a junction table between issues and labels
    # For now, return empty list
    return [] 