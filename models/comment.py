from flask import current_app

def get_db():
    return current_app.db

def create_comment(user_id, issue_id, content):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute(
            'INSERT INTO comments (user_id, issue_id, content, created_at) VALUES (%s, %s, %s, NOW()) RETURNING id', 
            (user_id, issue_id, content)
        )
        comment_id = cursor.fetchone()[0]
        db.engine.raw_connection().commit()
        return comment_id
    finally:
        cursor.close()

def get_comments_by_issue(issue_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('SELECT * FROM comments WHERE issue_id = %s', (issue_id,))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    finally:
        cursor.close()

def update_comment(comment_id, content):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('UPDATE comments SET content = %s WHERE id = %s', (content, comment_id))
        db.engine.raw_connection().commit()
    finally:
        cursor.close()

def delete_comment(comment_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('DELETE FROM comments WHERE id = %s', (comment_id,))
        db.engine.raw_connection().commit()
    finally:
        cursor.close() 