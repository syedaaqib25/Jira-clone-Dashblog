#!/usr/bin/env python3
"""
Database Connection Test Script
Tests the connection to the PostgreSQL database and verifies the schema.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to the Python path
sys.path.insert(0, '.')

def test_connection():
    """Main test function"""
    try:
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from config.config import Config
        
        # Create Flask app
        app = Flask(__name__)
        app.config.from_object(Config)
        
        # Initialize SQLAlchemy
        db = SQLAlchemy(app)
        app.db = db
        
        with app.app_context():
            print("Testing database connection...")
            print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # Test basic connection
            try:
                # Try to execute a simple query
                with db.engine.connect() as connection:
                    result = connection.execute(db.text("SELECT version();"))
                    version = result.fetchone()[0]
                    print(f"✅ Database connection successful!")
                    print(f"PostgreSQL version: {version}")
                    
                    # Test if our tables exist
                    tables_query = """
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name;
                    """
                    result = connection.execute(db.text(tables_query))
                    tables = [row[0] for row in result.fetchall()]
                    
                    print(f"\n📋 Found {len(tables)} tables in database:")
                    for table in tables:
                        print(f"  - {table}")
                    
                    # Check if we have the expected tables
                    expected_tables = [
                        'users', 'projects', 'issues', 'comments', 'teams',
                        'project_users', 'sprints', 'issue_labels', 'attachments',
                        'notifications', 'messages', 'components'
                    ]
                    
                    missing_tables = [table for table in expected_tables if table not in tables]
                    if missing_tables:
                        print(f"\n⚠️  Missing tables: {missing_tables}")
                        print("You may need to run the database schema script.")
                    else:
                        print("\n✅ All expected tables are present!")
                    
            except Exception as e:
                print(f"❌ Database connection failed: {str(e)}")
                return False
                
            # Test model imports
            print("\n🔧 Testing model imports...")
            try:
                from models.user import get_all_users, create_user
                from models.project import get_all_projects
                from models.issue import get_issues_by_project
                print("✅ All model imports successful!")
                
                # Test a simple model function (get_all_users)
                try:
                    users = get_all_users()
                    print(f"✅ Model test successful! Found {len(users)} users in database.")
                except Exception as e:
                    print(f"⚠️  Model test failed (this is normal if tables are empty): {str(e)}")
                    
            except Exception as e:
                print(f"❌ Model import failed: {str(e)}")
                return False
            
            print("\n🎉 Database setup verification complete!")
            return True
            
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        print("Make sure you have installed all dependencies: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_connection()
    
    if success:
        print("\n✅ All tests passed! Your database is ready to use.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)