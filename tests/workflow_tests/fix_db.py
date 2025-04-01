import os
import sys
import logging
from app import db, app

DB_PATH = "/root/socialme/social-me-test-2/app/instance/socialme.db"

logging.basicConfig(filename="db_fix.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def check_db_path():
    """Ensure database file exists."""
    if not os.path.exists(DB_PATH):
        logging.warning("Database file not found. Creating a new one...")
        try:
            with app.app_context():
                db.create_all()
            logging.info("✅ Database successfully created!")
        except Exception as e:
            logging.error(f"❌ Failed to create database: {e}")
            sys.exit(1)

def fix_permissions():
    """Ensure Flask can access the database."""
    try:
        os.chmod(DB_PATH, 0o777)
        logging.info("✅ Permissions fixed.")
    except Exception as e:
        logging.error(f"❌ Failed to set permissions: {e}")

def check_sqlalchemy_uri():
    """Ensure correct SQLAlchemy path."""
    expected_uri = f"sqlite:///{DB_PATH}"
    if app.config["SQLALCHEMY_DATABASE_URI"] != expected_uri:
        logging.warning(f"⚠️ SQLAlchemy URI incorrect: {app.config['SQLALCHEMY_DATABASE_URI']}")
        app.config["SQLALCHEMY_DATABASE_URI"] = expected_uri
        logging.info(f"✅ SQLAlchemy URI updated to: {expected_uri}")

def main():
    logging.info("🔍 Running Database Fix Script...")
    check_db_path()
    fix_permissions()
    check_sqlalchemy_uri()
    logging.info("✅ All fixes applied. Restart Flask.")

if __name__ == "__main__":
    main()
