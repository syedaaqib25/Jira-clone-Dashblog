from flask import current_app

def get_db():
    return current_app.db

def create_attachment(issue_id, filename, file_path, uploaded_by):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute(
            'INSERT INTO attachments (issue_id, filename, file_path, uploaded_by, uploaded_at) VALUES (%s, %s, %s, %s, NOW()) RETURNING id', 
            (issue_id, filename, file_path, uploaded_by)
        )
        attachment_id = cursor.fetchone()[0]
        db.engine.raw_connection().commit()
        return attachment_id
    finally:
        cursor.close()

def get_attachments_by_issue(issue_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('SELECT * FROM attachments WHERE issue_id = %s', (issue_id,))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    finally:
        cursor.close()

def delete_attachment(attachment_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('DELETE FROM attachments WHERE id = %s', (attachment_id,))
        db.engine.raw_connection().commit()
    finally:
        cursor.close() 