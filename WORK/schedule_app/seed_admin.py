# seed_admin.py
import bcrypt
from db import init_db, SessionLocal
from models import User, RoleEnum

def create_admin(username: str, password: str):
    init_db()  # на всякий случай создаст таблицы
    db = SessionLocal()
    try:
        if db.query(User).filter_by(username=username).first():
            print(f"Пользователь {username} уже существует")
            return
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        admin = User(username=username, password_hash=pw_hash, role=RoleEnum.admin)
        db.add(admin)
        db.commit()
        print(f"Администратор {username} успешно создан")
    finally:
        db.close()
        SessionLocal.remove()

if __name__ == "__main__":
    # Задайте здесь свои логин и пароль
    create_admin("admin", "Admin1!!")
