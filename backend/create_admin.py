from sqlalchemy.orm import Session
from backend.core.database import SessionLocal, engine, Base
from backend.models.user import User
from backend.utils.security import get_password_hash
import sys

def create_user(username, password):
    db = SessionLocal()
    try:
        # Check if user already exists
        user = db.query(User).filter(User.username == username).first()
        if user:
            print(f"User {username} already exists.")
            return

        print(f"Creating user {username}...")
        hashed_password = get_password_hash(password)
        new_user = User(
            username=username,
            hashed_password=hashed_password,
            is_active=True
        )
        db.add(new_user)
        db.commit()
        print("User created successfully!")
    except Exception as e:
        print(f"Error creating user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python -m backend.create_admin <username> <password>")
        # Default fallback
        create_user("admin", "admin123")
    else:
        create_user(sys.argv[1], sys.argv[2])
