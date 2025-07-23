-- USERS
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role VARCHAR(20) CHECK (role IN ('admin', 'developer', 'reporter')) DEFAULT 'reporter',
    profile_image TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- PROJECTS
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_by INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ISSUES
CREATE TABLE issues (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    type VARCHAR(20) CHECK (type IN ('bug', 'feature', 'task')) DEFAULT 'task',
    status VARCHAR(20) CHECK (status IN ('todo', 'in_progress', 'done')) DEFAULT 'todo',
    priority VARCHAR(20) CHECK (priority IN ('low', 'medium', 'high')) DEFAULT 'medium',
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    reporter_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    assignee_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- COMMENTS
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    issue_id INTEGER REFERENCES issues(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- NOTIFICATIONS
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
