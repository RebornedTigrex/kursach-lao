from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.dialects.postgresql import TIME
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import psycopg2

# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/your_db")

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost/postgres"

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
    day_of_week = Column(Integer, nullable=False)  # 0 - понедельник, 6 - воскресенье
    start_time = Column(TIME, nullable=False)
    end_time = Column(TIME, nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    classroom_id = Column(Integer, ForeignKey("classrooms.id"))

    subject = relationship("Subject")
    teacher = relationship("Teacher")
    classroom = relationship("Classroom")

# Создание таблиц
def init_db():
    Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Фронтенд
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
def get_schedule(week_start: str = Query(...), group_id: int = 1):
    db = SessionLocal()
    # week_start: 'YYYY-MM-DD'
    # Для MVP: возвращаем все Schedule для недели (можно фильтровать по group_id)
    schedules = db.query(Schedule).all()
    result = []
    for s in schedules:
        result.append({
            "id": s.id,
            "row": s.day_of_week,  # Для MVP row = day_of_week
            "col": 1,              # Для MVP col = 1 (или вычислять по времени)
            "subject": s.subject.name if s.subject else "",
            "room": s.classroom.number if s.classroom else "",
            "teacher": s.teacher.full_name if s.teacher else "",
        })
    return result

@app.post("/api/schedule/")
def post_schedule(data: dict):
    db = SessionLocal()
    # data: week_start, row, col, subject, room, teacher
    # MVP: ищем по row/col, если есть - обновляем, иначе создаём
    subject = db.query(Subject).filter_by(name=data.get("subject")).first()
    teacher = db.query(Teacher).filter_by(full_name=data.get("teacher")).first()
    room = db.query(Classroom).filter_by(number=data.get("room")).first()
    sched = Schedule(
        day_of_week=data.get("row"),
        start_time=datetime.strptime("09:00", "%H:%M").time(),
        end_time=datetime.strptime("10:30", "%H:%M").time(),
        subject_id=subject.id if subject else None,
        teacher_id=teacher.id if teacher else None,
        classroom_id=room.id if room else None,
    )
    db.add(sched)
    db.commit()
    return {"status": "ok"}

@app.delete("/api/schedule/")
def delete_schedule(week_start: str = Query(...), row: int = Query(...), col: int = Query(...)):
    db = SessionLocal()
    # MVP: удаляем по day_of_week=row
    sched = db.query(Schedule).filter_by(day_of_week=row).first()
    if sched:
        db.delete(sched)
        db.commit()
    return {"status": "ok"}



'''
Как использовать:

В начале работы выставьте window.DATA_SOURCE = "sql" или "localstorage" в консоли браузера или прямо в js-файле.
Запустите run_web.py — он поднимет backend и откроет веб-интерфейс.
Теперь можно работать с расписанием через SQL или localStorage, переключая источник данных одной переменной.
Примечание: Для полноценной работы с SQL потребуется доработать API (например, корректно определять row/col, start_time/end_time, group_id и т.д.), а также заполнить таблицы subjects, teachers, classrooms начальными данными.
'''