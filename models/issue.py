from flask import current_app

def get_db():
    return current_app.db

def create_issue(title, description, type_, status, priority, assignee_id, reporter_id, project_id, due_date, sprint_id=None):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('''
            INSERT INTO issues (title, description, type, status, priority, assignee_id, reporter_id, project_id, created_at, due_date, sprint_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s) RETURNING id
        ''', (title, description, type_, status, priority, assignee_id, reporter_id, project_id, due_date, sprint_id))
        issue_id = cursor.fetchone()[0]
        db.engine.raw_connection().commit()
        return issue_id
    finally:
        cursor.close()

def get_issue_by_id(issue_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('SELECT * FROM issues WHERE id = %s', (issue_id,))
        row = cursor.fetchone()
        if row:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
        return None
    finally:
        cursor.close()

def get_issues_by_project(project_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute("""
            SELECT i.*, u.name as assignee_name
            FROM issues i
            LEFT JOIN users u ON i.assignee_id = u.id
            WHERE i.project_id = %s
            ORDER BY i.status, i.priority DESC, i.id DESC
        """, (project_id,))
        
        rows = cursor.fetchall()
        if not cursor.description:
            return []

        columns = [desc[0] for desc in cursor.description]
        issues = []
        for row in rows:
            issue = dict(zip(columns, row))
            issue['assignee_name'] = row[-1] if row[-1] else None
            issues.append(issue)

        return issues
    finally:
        cursor.close()

def update_issue(issue_id, title, description, type_, status, priority, assignee_id, due_date, sprint_id=None):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('''
            UPDATE issues
            SET title = %s, description = %s, type = %s, status = %s, priority = %s, assignee_id = %s, due_date = %s, sprint_id = %s
            WHERE id = %s
        ''', (title, description, type_, status, priority, assignee_id, due_date, sprint_id, issue_id))
        db.engine.raw_connection().commit()
    finally:
        cursor.close()

def delete_issue(issue_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('DELETE FROM issues WHERE id = %s', (issue_id,))
        db.engine.raw_connection().commit()
    finally:
        cursor.close()

def get_issues_by_sprint(sprint_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute("""
            SELECT i.*, u.name as assignee_name
            FROM issues i
            LEFT JOIN users u ON i.assignee_id = u.id
            WHERE i.sprint_id = %s
            ORDER BY i.status, i.priority DESC
        """, (sprint_id,))
        
        rows = cursor.fetchall()
        if not cursor.description:
            return []

        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    finally:
        cursor.close()

def assign_issue_to_sprint(issue_id, sprint_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('UPDATE issues SET sprint_id = %s WHERE id = %s', (sprint_id, issue_id))
        db.engine.raw_connection().commit()
    finally:
        cursor.close()

def unassign_issue_from_sprint(issue_id):
    db = get_db()
    cursor = db.engine.raw_connection().cursor()
    try:
        cursor.execute('UPDATE issues SET sprint_id = NULL WHERE id = %s', (issue_id,))
        db.engine.raw_connection().commit()
    finally:
        cursor.close()