from flask import current_app

def get_db():
    return current_app.db

def create_notification(user_id, message):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute(
            "INSERT INTO notifications (user_id, message, created_at) VALUES (%s, %s, NOW()) RETURNING id",
            (user_id, message)
        )
        notification_id = cursor.fetchone()[0]
        db.engine.raw_connection().commit()
        return notification_id
    finally:
        cursor.close()

def get_notifications(user_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute(
            "SELECT * FROM notifications WHERE user_id = %s ORDER BY created_at DESC",
            (user_id,)
        )
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    finally:
        cursor.close()

def mark_notification_read(notification_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute(
            "UPDATE notifications SET is_read = TRUE WHERE id = %s",
            (notification_id,)
        )
        db.engine.raw_connection().commit()
    finally:
        cursor.close()

def get_unread_notifications(user_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute(
            "SELECT * FROM notifications WHERE user_id = %s AND is_read = FALSE ORDER BY created_at DESC",
            (user_id,)
        )
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    finally:
        cursor.close()

def delete_notification(notification_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute("DELETE FROM notifications WHERE id = %s", (notification_id,))
        db.engine.raw_connection().commit()
    finally:
        cursor.close()
