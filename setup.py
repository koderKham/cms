#!/usr/bin/env python
"""
Law Firm CMS Setup Script
This script sets up the Law Firm CMS application for first-time use.
It creates the database, applies migrations, and creates an admin user.
"""

import os
import sys
import secrets
from datetime import datetime
from getpass import getpass


def setup_environment():
    """Create .env file with default settings"""
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(f"SECRET_KEY={secrets.token_hex(32)}\n")
            f.write("FLASK_APP=run.py\n")
            f.write("FLASK_ENV=development\n")
            f.write("LOG_LEVEL=INFO\n")
        print("Created .env file with default settings")


def setup_database():
    """Initialize the database and apply migrations"""
    try:
        from app import create_app, db
        from flask_migrate import upgrade, init, migrate

        app = create_app()
        with app.app_context():
            # Check if migration directory exists
            if not os.path.exists('migrations'):
                # Initialize migrations
                init()

            # Generate migration
            migrate(message="Initial database setup")

            # Apply migrations
            upgrade()

            print("Database initialized and migrations applied")
    except Exception as e:
        print(f"Error setting up database: {str(e)}")
        return False

    return True


def create_admin_user():
    """Create an admin user if none exists"""
    try:
        from app import create_app, db
        from app.models.user import User

        app = create_app()
        with app.app_context():
            # Check if any admin user exists
            if User.query.filter_by(role='admin').first():
                print("Admin user already exists")
                return True

            # Get admin user details
            print("\nCreate Administrator Account")
            print("--------------------------")
            name = input("Full Name: ")
            email = input("Email: ")

            while True:
                password = getpass("Password (min 8 characters): ")
                if len(password) < 8:
                    print("Password must be at least 8 characters long")
                    continue

                confirm = getpass("Confirm Password: ")
                if password != confirm:
                    print("Passwords don't match")
                    continue

                break

            # Create admin user
            admin = User(
                name=name,
                email=email,
                role='admin',
                created_at=datetime.utcnow()
            )
            admin.set_password(password)

            db.session.add(admin)
            db.session.commit()

            print(f"\nAdmin user '{email}' created successfully!")
    except Exception as e:
        print(f"Error creating admin user: {str(e)}")
        return False

    return True


def main():
    """Main setup function"""
    print("Law Firm CMS Setup")
    print("=================\n")

    # Setup environment
    setup_environment()

    # Setup database
    if not setup_database():
        print("Database setup failed. Exiting.")
        sys.exit(1)

    # Create admin user
    if not create_admin_user():
        print("Admin user creation failed.")

    print("\nSetup completed successfully!")
    print("\nYou can now run the application:")
    print("  python run.py")
    print("  # or")
    print("  flask run")


if __name__ == "__main__":
    main()