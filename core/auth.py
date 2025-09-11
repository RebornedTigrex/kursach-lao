from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy.testing.pickleable import User
from db_work import Auth, SessionLocal, init_db, engine, connect_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_password(input_password: str, stored_password: str) -> bool:
    return bcrypt.checkpw(input_password.encode("utf-8"), stored_password.encode("utf-8"))


def registration_user():
    """ Регистрация пользователя """
    with SessionLocal() as db: # ПОКА костыль пока нету эндпоинта и декоратора от FastApi
        user, password = input("Введите имя пользователя и пароль через пробел: ").split()
        if db.query(Auth).filter(Auth.user == user).first():
            raise HTTPException(status_code = 401, detail = "This username already exists")
        hashed_password = hash_password(password)
        auth = Auth(user = user, password_hash = hashed_password)
        db.add(auth)
        db.commit()
        return {"access_token": user, "token_type": "bearer"}


def authorization_user():
    """ Авторизация юзера """
    with SessionLocal() as db: # ПОКА костыль пока нету эндпоинта и декоратора от FastApi
        username, password = input("Введите имя пользователя и пароль через пробел: ").split()
        user = db.query(Auth).filter(Auth.user == username).first()
        if not user:
            raise HTTPException(status_code = 400, detail = "Incorrect username or password")
        if check_password(password, user.password_hash):
            return {"access_token": user.user, "token_type": "bearer"}
        else:
            raise HTTPException(status_code = 400, detail = "Incorrect username or password")


if __name__ == "__main__":
    import os

    init_db()
    with SessionLocal() as db:
        test_v: str = input("Введите 1 для Регистрация юзера иначе авторизация: ")
        test_d: dict
        if test_v == "1":
            test_d = registration_user()
        else:
            auth = Auth(user = "lox", password_hash = hash_password("1234"))
            db.add(auth)
            db.commit()
            print(f"данные для входа: user={auth.user}, pass=1234")
            test_d = authorization_user()
        lst = [f"id = {x.id}, user = {x.user}, passworrd = {x.password_hash}" for x in db.query(Auth).all()]
        print(f"функция вернула: {test_d}, в таблице Auth щас: {lst}")
        db.close()

    engine.dispose()
    try:
        os.remove("database.db")
        print("Бд нахуй снесена")
    except Exception as e:
        print("Ёптыть бд не удолилась", e)
