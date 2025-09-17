from datetime import datetime, timezone, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from sqlalchemy.testing.pickleable import User
from db_work import Auth, SessionLocal, init_db, engine, connect_db, Token

ALGORITHM = "HS256"
SECRET_KEY = "5c6a5cc4dd658887b26ea94b9b644b8e5f535319924b48e642b3f1ba2612a81d"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

text_incorrect = "Incorrect username or password"


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_password(input_password: str, stored_password: str) -> bool:
    return bcrypt.checkpw(input_password.encode("utf-8"), stored_password.encode("utf-8"))


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """ создание токена """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes = 15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt


def registration_user() -> dict[str, str]:
    """ Регистрация пользователя """
    with SessionLocal() as db:  # ПОКА костыль пока нету эндпоинта и декоратора от FastApi
        user, password = input("Введите имя пользователя и пароль через пробел: ").split()
        if db.query(Auth).filter(Auth.user == user).first():
            raise HTTPException(status_code = 401, detail = "This username already exists")
        if not user or not password:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = text_incorrect,
                headers = {"WWW-Authenticate": "Bearer"},
            )
        hashed_password = hash_password(password)
        auth = Auth(user = user, password_hash = hashed_password)
        db.add(auth)
        db.flush()
        access_token_expires = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data = {"sub": auth.user}, expires_delta = access_token_expires
        )
        token = Token(uid = auth.id, token = access_token)
        db.add(token)
        db.commit()
        return {"access_token": access_token, "token_type": "bearer"}


def authorization_user():
    """ Авторизация юзера """
    with SessionLocal() as db:  # ПОКА костыль пока нету эндпоинта и декоратора от FastApi
        username, password = input("Введите имя пользователя и пароль через пробел: ").split()
        user = db.query(Auth).filter(Auth.user == username).first()
        if not user:
            raise HTTPException(status_code = 400, detail = text_incorrect)
        if check_password(password, user.password_hash):
            return {"access_token": user.token.token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code = 400, detail = text_incorrect)


if __name__ == "__main__":
    import os

    init_db()
    try:
        with SessionLocal() as db:
            test_v: str = input("Введите 1 для Регистрация юзера иначе авторизация: ")
            test_d: dict
            if test_v == "1":
                test_d = registration_user()
            else:
                auth = Auth(user = "lox", password_hash = hash_password("1234"))
                db.add(auth)
                db.flush()
                print(f"данные для входа: user={auth.user}, pass=1234")
                access_token_expires = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = create_access_token(
                    data = {"sub": auth.user}, expires_delta = access_token_expires
                )
                token = Token(uid = auth.id, token = access_token)
                db.add(token)
                db.commit()
                test_d = authorization_user()
            lst_a = [f"id = {x.id}, user = {x.user}, passworrd = {x.password_hash}" for x in db.query(Auth).all()]
            lst_t = [f"uid = {x.uid}, token = {x.token}" for x in db.query(Token).all()]
            print(f"функция вернула: {test_d}\nв таблице Auth щас: {lst_a}\nв таблице Token щас: {lst_t}")

    except BaseException as base_e:
        raise base_e
    finally:
        db.close()
        engine.dispose()
        try:
            os.remove("database.db")
            print("Бд нахуй снесена")
        except Exception as e:
            print("Ёптыть бд не удолилась", e)
