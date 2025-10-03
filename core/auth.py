import os
from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import IntegrityError
from typing import Optional, Dict, Any

import bcrypt
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, InstrumentedAttribute

from core.db_work import Auth, connect_db

SECRET_KEY = os.getenv("SECRET_KEY", r"../.env")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set. Set it in environment or in .env before running the app.")

ALGORITHM = os.getenv("ALGORITHM", "HS256")

try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
except ValueError:
    ACCESS_TOKEN_EXPIRE_MINUTES = 15

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/api/auth")

text_user_exists = "Username already exists"


def hash_password(password: str) -> str:
    """Возвращает закодированный хэш пароля (str)."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_password(input_password: str, stored_password: str) -> bool:
    """Проверяет plain password против хэша."""
    return bcrypt.checkpw(input_password.encode("utf-8"), stored_password.encode("utf-8"))


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """ Создаёт JWT с полем exp и iat.
    :param data: содержит {"sub": username} или {"sub": user_id}.
    :return: Возвращает строку токена.
    """
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"iat": now, "exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return token


def verify_access_token(token: str) -> Dict[str, Any]:
    """
    Декодирует и проверяет токен.
    В случае ошибки бросает HTTPException 401.
    :return Возвращает payload (словарь).
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Token expired")
    except InvalidTokenError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid token")
    return payload


def get_current_user(db: Session = Depends(connect_db), token: str = Depends(oauth2_scheme)) -> dict[
    str, Any]:
    """
    Зависимость для эндпоинтов FastAPI.
    Проверяет токен, находит пользователя в БД и возвращает ORM-объект Auth.
    Бросает HTTPException(401) при любой ошибке.
    """
    payload = verify_access_token(token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid token payload")

    user = db.query(Auth).filter(Auth.user == username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "User not found")
    return {"username": user.user, "id": user.id}


def register_user(db: Session, username: str, password: str) -> tuple[str, "Auth"]:
    """
    Создаёт пользователя в БД. Если пользователь существует — бросает HTTPException(400).
    :return: (access_token: str , user: Auth, соотвествующая запись в таблице)
    """
    if db.query(Auth).filter(Auth.user == username).first():
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = text_user_exists)

    hashed = hash_password(password)
    user = Auth(user = username, password_hash = hashed)
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
        access_token = create_access_token(
            data = {"sub": user.user},
            expires_delta = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = text_user_exists)

    return access_token, user


def authenticate_user(db: Session, username: str, password: str) -> str:
    """
    Аутентификация: проверяет логин/пароль.
    Бросает HTTPException(401) при неверных данных.
    :return: возвращает access token (JWT).
    """
    user = db.query(Auth).filter(Auth.user == username).first()
    if not user or not check_password(password, user.password_hash):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Incorrect username or password")

    access_token = create_access_token(
        data = {"sub": user.user},
        expires_delta = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return access_token
