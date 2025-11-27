from fastapi import FastAPI, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from sqlalchemy.orm import Session
import asyncio

from core.db_work import init_db, connect_db, SessionLocal
from core.services import *
from core.auth import get_current_user

init_db()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://127.0.0.1:8000", "http://127.0.0.1:3000"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


def _run_with_session(func, *args, **kwargs):
    """
    Создаёт отдельную SessionLocal внутри текущего (worker) потока,
    вызывает синхронную функцию func(db, *args, **kwargs) и закрывает сессию.
    Это гарантирует, что сессия используется в том же потоке, где создана.
    """
    db: Session = SessionLocal()
    try:
        return func(db, *args, **kwargs)
    finally:
        db.close()


# ==================== API ====================

"""Rooms"""


@app.get("/api/rooms/")
def get_rooms(db: Session = Depends(connect_db)):
    return s_get_rooms(db)


@app.post("/api/rooms/")
def post_room(data: str = Body(...), current_user: dict = Depends(get_current_user), db: Session = Depends(connect_db)):
    return s_post_room(db, current_user, data)


@app.delete("/api/rooms/")
def delete_room(id: int = Body(...), current_user: dict = Depends(get_current_user), db: Session = Depends(connect_db)):
    return s_delete_room(db, current_user, id)


"""Teachers"""


@app.get("/api/teachers/")
def get_teachers(db: Session = Depends(connect_db)):
    return s_get_teachers(db)


@app.post("/api/teachers/")
def post_teacher(data: str = Body(...), current_user: dict = Depends(get_current_user),
                 db: Session = Depends(connect_db)):
    return s_post_teacher(db, current_user, data)


@app.delete("/api/teachers/")
def delete_teacher(id: int = Body(...), current_user: dict = Depends(get_current_user),
                   db: Session = Depends(connect_db)):
    return s_delete_teacher(db, current_user, id)


"""Schedule"""


@app.get("/api/schedule/")
async def get_schedule():
    return await asyncio.to_thread(_run_with_session, s_get_schedule)


@app.post("/api/schedule/")
async def post_schedule(data: dict = Body(...), current_user: dict = Depends(get_current_user)):
    return await asyncio.to_thread(_run_with_session, s_post_schedule, current_user, data)


@app.delete("/api/schedule/")
async def delete_schedule(key: str = Body(...), current_user: dict = Depends(get_current_user)):
    return await asyncio.to_thread(_run_with_session, s_delete_schedule, current_user, key)


"""Subjects"""


@app.get("/api/subjects/")
def get_subjects(db: Session = Depends(connect_db)):
    return s_get_subjects(db)


@app.post("/api/subjects/")
def post_subject(data: str = Body(...), current_user: dict = Depends(get_current_user),
                 db: Session = Depends(connect_db)):
    return s_post_subject(db, current_user, data)


@app.delete("/api/subjects/")
def delete_subject(id: int = Body(...), current_user: dict = Depends(get_current_user),
                   db: Session = Depends(connect_db)):
    return s_delete_subject(db, current_user, id)


"""Register"""


@app.post("/api/register")
async def post_register(response: Response, data: dict = Body(...)):
    return await asyncio.to_thread(_run_with_session, s_post_register, data)


"""Auth"""


@app.post("/api/auth")
async def post_auth(response: Response, data: dict = Body(...)):
    return await asyncio.to_thread(_run_with_session, s_post_auth, data)