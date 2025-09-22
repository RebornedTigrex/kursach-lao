from fastapi import FastAPI, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db_work import init_db, connect_db
from services import *

init_db()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://127.0.0.1:8000", "http://127.0.0.1:3000"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


# ==================== API ====================

@app.get("/api/subjects/")
def get_subjects(db: Session = Depends(connect_db)):
    return s_get_subjects(db)


@app.get("/api/rooms/")
def get_rooms(db: Session = Depends(connect_db)):
    return s_get_rooms(db)


@app.get("/api/teachers/")
def get_teachers(db: Session = Depends(connect_db)):
    return s_get_teachers(db)


@app.get("/api/schedule/")
def get_schedule(db: Session = Depends(connect_db)):
    return s_get_schedule(db)


@app.post("/api/schedule/")
def post_schedule(data: dict, db: Session = Depends(connect_db)):
    return s_post_schedule(data, db)


@app.delete("/api/schedule/")
def delete_schedule(key: str = Body(...), db: Session = Depends(connect_db)):
    return s_delete_schedule(db, key)


@app.post("/api/subjects/")
def post_subject(data: str = Body(...), db: Session = Depends(connect_db)):
    return s_post_subject(db, data)


@app.delete("/api/subjects/")
def delete_subject(id: int = Body(...), db: Session = Depends(connect_db)):
    return s_delete_subject(db, id)


@app.post("/api/rooms/")
def post_room(data: str = Body(...), db: Session = Depends(connect_db)):
    return s_post_room(db, data)


@app.delete("/api/rooms/")
def delete_room(id: int = Body(...), db: Session = Depends(connect_db)):
    return s_delete_room(db, id)


@app.post("/api/teachers/")
def post_teacher(data: str = Body(...), db: Session = Depends(connect_db)):
    return s_post_teacher(db, data)


@app.delete("/api/teachers/")
def delete_teacher(id: int = Body(...), db: Session = Depends(connect_db)):
    return s_delete_teacher(db, id)


@app.post("/api/register")
def post_register(data: dict = Body(...), db: Session = Depends(connect_db)):
    return s_post_register(db, data)


@app.post("/api/auth")
def post_auth(data: dict = Body(...), db: Session = Depends(connect_db)):
    return s_post_auth(db, data)
