from flask import current_app
from datetime import datetime

def get_db():
    return current_app.db

def create_message(sender_id, receiver_id, content, project_id=None):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute("""
            INSERT INTO messages (sender_id, receiver_id, content, project_id, created_at)
            VALUES (%s, %s, %s, %s, NOW()) RETURNING id
        """, (sender_id, receiver_id, content, project_id))
        message_id = cursor.fetchone()[0]
        db.engine.raw_connection().commit()
        return message_id
    finally:
        cursor.close()

def get_inbox(user_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute("""
            SELECT m.id, u_from.name as sender_name, u_to.name as receiver_name, 
                   m.content, m.created_at, m.project_id
            FROM messages m
            JOIN users u_from ON m.sender_id = u_from.id
            JOIN users u_to ON m.receiver_id = u_to.id
            WHERE m.receiver_id = %s
            ORDER BY m.created_at DESC
        """, (user_id,))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    finally:
        cursor.close()

def get_sent(user_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute("""
            SELECT m.id, u_from.name as sender_name, u_to.name as receiver_name, 
                   m.content, m.created_at, m.project_id
            FROM messages m
            JOIN users u_from ON m.sender_id = u_from.id
            JOIN users u_to ON m.receiver_id = u_to.id
            WHERE m.sender_id = %s
            ORDER BY m.created_at DESC
        """, (user_id,))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    finally:
        cursor.close()

def get_all_messages():
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute("""
            SELECT m.id, u_from.name as sender_name, u_to.name as receiver_name, 
                   m.content, m.created_at, m.project_id
            FROM messages m
            JOIN users u_from ON m.sender_id = u_from.id
            JOIN users u_to ON m.receiver_id = u_to.id
            ORDER BY m.created_at DESC
        """)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    finally:
        cursor.close()

def delete_message(message_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute("DELETE FROM messages WHERE id = %s", (message_id,))
        db.engine.raw_connection().commit()
    finally:
        cursor.close() 