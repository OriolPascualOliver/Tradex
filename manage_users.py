import argparse
import os
import sys

# Ensure internal modules are importable
BASE_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(BASE_DIR, "backend"))

# Default to SQLite if no DB configured
os.environ.setdefault("DATABASE_URL", "sqlite:///./sql_app.db")

from backend.core.database import SessionLocal, Base, engine
from backend.api.models.user import User
from passlib.context import CryptContext

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(email: str, password: str) -> None:
    db = SessionLocal()
    try:
        if db.query(User).filter_by(email=email).first():
            print("User already exists")
            return
        user = User(email=email, hashed_password=pwd_context.hash(password))
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Created user {email} with id {user.id}")
    finally:
        db.close()


def update_password(email: str, password: str) -> None:
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(email=email).first()
        if not user:
            print("User not found")
            return
        user.hashed_password = pwd_context.hash(password)
        db.commit()
        print(f"Password updated for {email}")
    finally:
        db.close()


def delete_user(email: str) -> None:
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(email=email).first()
        if not user:
            print("User not found")
            return
        db.delete(user)
        db.commit()
        print(f"Deleted user {email}")
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage user accounts")
    sub = parser.add_subparsers(dest="command", required=True)

    p_create = sub.add_parser("create", help="Create a new user")
    p_create.add_argument("email")
    p_create.add_argument("password")

    p_update = sub.add_parser("update", help="Update a user's password")
    p_update.add_argument("email")
    p_update.add_argument("password")

    p_delete = sub.add_parser("delete", help="Delete a user")
    p_delete.add_argument("email")

    args = parser.parse_args()
    if args.command == "create":
        create_user(args.email, args.password)
    elif args.command == "update":
        update_password(args.email, args.password)
    elif args.command == "delete":
        delete_user(args.email)


if __name__ == "__main__":
    main()
