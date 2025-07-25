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
SECRET_KEY=your-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production
DATABASE_URL=postgresql://username:password@localhost:5432/jira_clone_db
UPLOAD_FOLDER=static/uploads
EOF
    echo ".env file created. Please update the values with your actual configuration."
fi

echo "Setup complete!"
echo ""
echo "To run the application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Set up your PostgreSQL database and update DATABASE_URL in .env"
echo "3. Run the database schema: psql -d your_database -f database_schema.sql"
echo "4. Start the application: python app.py"
echo ""
echo "Don't forget to:"
echo "- Update SECRET_KEY and JWT_SECRET_KEY in .env with secure random values"
echo "- Configure your PostgreSQL database connection"
echo "- Set up proper environment variables for production deployment"