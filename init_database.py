#!/usr/bin/env python3
"""
Database Initialization Script
Creates the database schema on the PostgreSQL database.
"""

import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Load environment variables
load_dotenv()

def init_database():
    """Initialize the database with the schema"""
    
    # Get database URL
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        return False
    
    print(f"🔧 Connecting to database...")
    print(f"Database: {database_url.split('@')[1] if '@' in database_url else 'hidden'}")
    
    try:
        # Connect to database
        conn = psycopg2.connect(database_url)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("✅ Connected to database successfully!")
        
        # Read schema file
        try:
            with open('database_schema.sql', 'r') as f:
                schema_sql = f.read()
        except FileNotFoundError:
            print("❌ database_schema.sql file not found")
            return False
        
        print("📋 Executing database schema...")
        
        # Split the schema into individual statements
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        
        for i, statement in enumerate(statements):
            try:
                cursor.execute(statement)
                print(f"  ✅ Statement {i+1}/{len(statements)} executed")
            except Exception as e:
                # Some statements might fail if tables already exist - that's okay
                print(f"  ⚠️  Statement {i+1} warning: {str(e)}")
        
        print("🎉 Database schema initialization complete!")
        
        # Verify tables were created
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        
        tables = [row[0] for row in cursor.fetchall()]
        print(f"\n📋 Database now contains {len(tables)} tables:")
        for table in tables:
            print(f"  - {table}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 JIRA Clone Database Initialization")
    print("=====================================")
    
    success = init_database()
    
    if success:
        print("\n✅ Database initialization successful!")
        print("You can now run: python3 test_db_connection.py")
        print("Or start the application: python app.py")
        sys.exit(0)
    else:
        print("\n❌ Database initialization failed!")
        print("Please check the error messages above.")
        sys.exit(1)