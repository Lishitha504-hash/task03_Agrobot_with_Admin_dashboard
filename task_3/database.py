import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

# -------------------------------
# MODELS
# -------------------------------

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100))
    role = db.Column(db.String(20), default="farmer")
    primary_crop = db.Column(db.String(100))
    region = db.Column(db.String(100))
    preferred_language = db.Column(db.String(20), default="en")

class ChatHistory(db.Model):
    __tablename__ = "chat_history"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    user_message = db.Column(db.Text)
    bot_response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    feedback = db.Column(db.String(20), nullable=True)

# -------------------------------
# DATABASE INITIALIZATION
# -------------------------------

def init_db(app):
    """Initialize the database and create a default admin user if needed."""
    db_path = os.path.join(os.path.dirname(__file__), "..", "agrobot.db")
    db_uri = f"sqlite:///{os.path.abspath(db_path)}"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        # If corrupted or invalid, remove and recreate DB
        if os.path.exists(db_path):
            try:
                import sqlite3
                conn = sqlite3.connect(db_path)
                conn.execute("PRAGMA integrity_check;")
                conn.close()
            except Exception:
                print("⚠️ Detected a corrupted database — recreating agrobot.db...")
                os.remove(db_path)

        db.create_all()

        # Create default admin if missing
        admin_email = os.getenv("ADMIN_EMAIL", "admin@agrobot.com")
        admin_password = os.getenv("ADMIN_PASSWORD", "Admin@123")

        if not User.query.filter_by(email=admin_email).first():
            admin = User(
                email=admin_email,
                password=generate_password_hash(admin_password),
                name="Administrator",
                role="admin",
                preferred_language="en"
            )
            db.session.add(admin)
            db.session.commit()
            print(f"✅ Created default admin: {admin_email}")

    return db
