from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from fastapi import FastAPI, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)

class Classroom(Base):
    __tablename__ = "classrooms"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, nullable=False)

class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True, index=True)
    datekey = Column(String)
    dateMon = Column(Date, nullable=False)  # дата пары по понедельникам
    lesson_number = Column(Integer, nullable=False)  # номер пары (например, 3)
    day_of_week = Column(Integer, nullable=False)   # номер дня недели (например, 2)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    classroom_id = Column(Integer, ForeignKey("classrooms.id"))

    subject = relationship("Subject")
    teacher = relationship("Teacher")
    classroom = relationship("Classroom")

# Создание таблиц

def init_db():
    Base.metadata.create_all(bind=engine)
    
init_db()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== API ====================

@app.get("/api/subjects/")
def get_subjects():
    db = SessionLocal()
    subjects = db.query(Subject).all()
    return [{"id": s.id, "name": s.name} for s in subjects]

@app.get("/api/rooms/")
def get_rooms():
    db = SessionLocal()
    rooms = db.query(Classroom).all()
    return [{"id": r.id, "number": r.number} for r in rooms]

@app.get("/api/teachers/")
def get_teachers():
    db = SessionLocal()
    teachers = db.query(Teacher).all()
    return [{"id": t.id, "full_name": t.full_name} for t in teachers]

@app.get("/api/schedule/")
def get_schedule():
    db = SessionLocal()
    schedules = db.query(Schedule).all()
    result = {}
    for s in schedules:
        key = str(s.datekey)
        print(f"Processing schedule for key: {key}")
        result[key] = {
            "subject": s.subject.name if s.subject else "",
            "room": s.classroom.number if s.classroom else "",
            "teacher": s.teacher.full_name if s.teacher else ""
        }
        print(f"Added schedule for {key}: {result[key]}")
    print(f"Final schedule result: {result}")
    return result

@app.post("/api/schedule/")
def post_schedule(data: dict):
    print(data)
    db = SessionLocal()
    datekey = list(data.keys())[0]
    print(datekey)
    # data: {"2025-06-09_3_2": {"subject":..., "room":..., "teacher":...}, ...}
    for key, value in data.items():
        try:
            date_str, lesson_number, day_of_week = key.split('_')
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            lesson_number = int(lesson_number)
            day_of_week = int(day_of_week)
        except Exception:
            continue
        subject = db.query(Subject).filter_by(name=value.get("subject")).first()
        teacher = db.query(Teacher).filter_by(full_name=value.get("teacher")).first()
        room = db.query(Classroom).filter_by(number=value.get("room")).first()
        sched = Schedule(
            datekey=datekey,
            dateMon=date_obj,
            lesson_number=lesson_number,
            day_of_week=day_of_week,
            subject_id=subject.id if subject else None,
            teacher_id=teacher.id if teacher else None,
            classroom_id=room.id if room else None,
        )
        db.add(sched)
    db.commit()
    return {"status": "ok"}

@app.delete("/api/schedule/")
def delete_schedule(key: str = Body(...)):
    db = SessionLocal()
    sched = db.query(Schedule).filter_by(datekey=key).first()
    if sched:
        db.delete(sched)
        db.commit()
        return {"status": "ok"}
    else:
        return {"status": "error", "msg": "invalid key"}

@app.post("/api/subjects/")
def post_subject(data: str = Body(...)):
    db = SessionLocal()
    name = data
    if not name:
        return {"status": "error", "msg": "name required"}
    subject = Subject(name=name)
    db.add(subject)
    db.commit()
    return {"status": "ok", "id": subject.id}

@app.delete("/api/subjects/")
def delete_subject(id: int = Body(...)):
    db = SessionLocal()
    subject = db.query(Subject).filter_by(id=id).first()
    if subject:
        db.delete(subject)
        db.commit()
    return {"status": "ok"}

@app.post("/api/rooms/")
def post_room(data: str = Body(...)):
    db = SessionLocal()
    number = data
    if not number:
        return {"status": "error", "msg": "number required"}
    room = Classroom(number=number)
    db.add(room)
    db.commit()
    return {"status": "ok", "id": room.id}

@app.delete("/api/rooms/")
def delete_room(id: int = Body(...)):
    print(f"Deleting room with id: {id}")
    db = SessionLocal()
    room = db.query(Classroom).filter_by(id=id).first()
    if room:
        db.delete(room)
        db.commit()
    return {"status": "ok"}

@app.post("/api/teachers/")
def post_teacher(data: str = Body(...)):
    db = SessionLocal()
    full_name = data
    if not full_name:
        return {"status": "error", "msg": "full_name required"}
    teacher = Teacher(full_name=full_name)
    db.add(teacher)
    db.commit()
    return {"status": "ok", "id": teacher.id}

@app.delete("/api/teachers/")
def delete_teacher(id: int = Body(...)):
    db = SessionLocal()
    teacher = db.query(Teacher).filter_by(id=id).first()
    if teacher:
        db.delete(teacher)
        db.commit()
    return {"status": "ok"}
