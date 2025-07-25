#!/bin/bash

# JIRA Clone Setup Script
echo "Setting up JIRA Clone application..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is required but not installed. Please install pip3 and try again."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production

# Database Configuration
DATABASE_URL=postgresql://jira_clone_db_user:OKdnwVe8v6SWtqCPKTSjZ0lkRdZYLMWJ@dpg-d1vku07gi27c738clt1g-a.oregon-postgres.render.com/jira_clone_db

# File Upload Configuration
UPLOAD_FOLDER=static/uploads

# Flask Environment
FLASK_ENV=development
FLASK_DEBUG=1
EOF
    echo ".env file created with your Render PostgreSQL database configuration."
fi

echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Test the database connection: python3 test_db_connection.py"
echo "2. If tables are missing, run the schema: psql <DATABASE_URL> -f database_schema.sql"
echo "3. Start the application: python app.py"
echo ""
echo "Your application is configured to use:"
echo "- Render PostgreSQL database (already configured)"
echo "- PostgreSQL driver (psycopg2-binary)"
echo "- All models updated for PostgreSQL compatibility"
echo ""
echo "⚠️  IMPORTANT: Update SECRET_KEY and JWT_SECRET_KEY in .env with secure random values before production deployment!"