from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import time
from typing import List
import models
import database
from pydantic import BaseModel

app = FastAPI()

# Настройки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модели Pydantic для запросов/ответов
class SubjectCreate(BaseModel):
    name: str

class TeacherCreate(BaseModel):
    full_name: str
    subject_ids: List[int] = []

class ClassroomCreate(BaseModel):
    number: str
    building: str = None
    capacity: int = None

class ScheduleCreate(BaseModel):
    day_of_week: int  # 0-6 (пн-вс)
    start_time: str  # "HH:MM"
    end_time: str    # "HH:MM"
    group_id: int
    subject_id: int
    teacher_id: int
    classroom_id: int

@app.on_event("startup")
def startup():
    models.init_db()

# API endpoints
@app.post("/subjects/")
def create_subject(subject: SubjectCreate, db: Session = Depends(database.get_db)):
    return database.DBActions.create_subject(db, subject.name)

@app.post("/teachers/")
def create_teacher(teacher: TeacherCreate, db: Session = Depends(database.get_db)):
    return database.DBActions.create_teacher(db, teacher.full_name, teacher.subject_ids)

@app.post("/classrooms/")
def create_classroom(classroom: ClassroomCreate, db: Session = Depends(database.get_db)):
    return database.DBActions.create_classroom(
        db, classroom.number, classroom.building, classroom.capacity
    )

@app.post("/schedules/")
def create_schedule(schedule: ScheduleCreate, db: Session = Depends(database.get_db)):
    try:
        start_time = time.fromisoformat(schedule.start_time)
        end_time = time.fromisoformat(schedule.end_time)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid time format. Use HH:MM")
    
    return database.DBActions.create_schedule(
        db,
        schedule.day_of_week,
        start_time,
        end_time,
        schedule.group_id,
        schedule.subject_id,
        schedule.teacher_id,
        schedule.classroom_id
    )

@app.get("/groups/{group_id}/schedule/")
def get_group_schedule(group_id: int, week_offset: int = 0, db: Session = Depends(database.get_db)):
    schedules = database.DBActions.get_group_schedule(db, group_id, week_offset)
    return {"group_id": group_id, "schedules": schedules}

@app.get("/teachers/{teacher_id}/schedule/")
def get_teacher_schedule(teacher_id: int, week_offset: int = 0, db: Session = Depends(database.get_db)):
    schedules = database.DBActions.get_teacher_schedule(db, teacher_id, week_offset)
    return {"teacher_id": teacher_id, "schedules": schedules}

@app.get("/classrooms/{classroom_id}/schedule/")
def get_classroom_schedule(classroom_id: int, week_offset: int = 0, db: Session = Depends(database.get_db)):
    schedules = database.DBActions.get_classroom_schedule(db, classroom_id, week_offset)
    return {"classroom_id": classroom_id, "schedules": schedules}