import sys
import os
from sqlalchemy.orm import Session

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.core.database import SessionLocal, engine, Base
from backend.models.user import User
from backend.utils.security import get_password_hash

def create_user(username, password):
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user:
            print(f"User {username} already exists.")
            return
        
        new_user = User(
            username=username,
            hashed_password=get_password_hash(password),
            is_active=True
        )
        db.add(new_user)
        db.commit()
        print(f"User {username} created successfully.")
    except Exception as e:
        print(f"Error creating user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scripts/create_user.py <username> <password>")
    else:
        create_user(sys.argv[1], sys.argv[2])
