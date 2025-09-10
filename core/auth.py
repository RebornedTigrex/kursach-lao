from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
import bcrypt
from sqlalchemy.testing.pickleable import User
from db_work import Auth, SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def check_password(input_password: str, stored_password: str) -> bool:
    return bcrypt.checkpw(input_password.encode("utf-8"), stored_password.encode("utf-8"))


def authenticate_user():
    """ Регистрация пользователя """
    db = SessionLocal()
    user, password = input("Введите имя юзера и пароль через пробел: ").split()
    if False:  # хз проверка какая-то
        raise HTTPException(status_code = 400, detail = "Incorrect username or password")
    hashed_password = hash_password(password)
    auth = Auth(user = user, password_hash = hashed_password.decode("utf-8"))
    db.add(auth)
    db.commit()
    return {"access_token": user, "token_type": "bearer"}
