from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/your_db")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite:///database.db"

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
    day_of_week = Column(Integer, nullable=False)
    col = Column(Integer, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
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
    allow_origins=["http://127.0.0.1:3000"],  # Фронтенд
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== API ====================

# Декоратор для явной поддержки OPTIONS
def allow_options(route):
    async def options_handler(request):
        return {"message": "OPTIONS allowed"}
    route.options = options_handler
    return route


class EntityCreate(BaseModel):
    name: str = None
    number: str = None
    full_name: str = None

# ==================== API: Subjects ====================
@app.get("/api/subjects/", response_model=list)
@allow_options
def get_subjects():
    db = SessionLocal()
    try:
        subjects = db.query(Subject).all()
        return [{"id": s.id, "name": s.name} for s in subjects]
    finally:
        db.close()

@app.post("/api/subjects/")
@allow_options
def add_subject(data: EntityCreate):
    db = SessionLocal()
    try:
        if not data.name:
            raise HTTPException(status_code=400, detail="Subject name is required")
        subject = Subject(name=data.name)
        db.add(subject)
        db.commit()
        db.refresh(subject)
        return {"id": subject.id, "name": subject.name}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add subject: {str(e)}")
    finally:
        db.close()

@app.delete("/api/subjects/{name}/")
@allow_options
def delete_subject(name: str):
    db = SessionLocal()
    try:
        subject = db.query(Subject).filter_by(name=name).first()
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        db.delete(subject)
        db.commit()
        return {"status": "ok"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete subject: {str(e)}")
    finally:
        db.close()

# ==================== API: Rooms ====================
@app.get("/api/rooms/", response_model=list)
@allow_options
def get_rooms():
    db = SessionLocal()
    try:
        rooms = db.query(Classroom).all()
        return [{"id": r.id, "number": r.number} for r in rooms]
    finally:
        db.close()

@app.post("/api/rooms/")
@allow_options
def add_room(data: EntityCreate):
    db = SessionLocal()
    try:
        if not data.number:
            raise HTTPException(status_code=400, detail="Room number is required")
        room = Classroom(number=data.number)
        db.add(room)
        db.commit()
        db.refresh(room)
        return {"id": room.id, "number": room.number}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add room: {str(e)}")
    finally:
        db.close()

@app.delete("/api/rooms/{number}/")
@allow_options
def delete_room(number: str):
    db = SessionLocal()
    try:
        room = db.query(Classroom).filter_by(number=number).first()
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        db.delete(room)
        db.commit()
        return {"status": "ok"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete room: {str(e)}")
    finally:
        db.close()

# ==================== API: Teachers ====================
@app.get("/api/teachers/", response_model=list)
@allow_options
def get_teachers():
    db = SessionLocal()
    try:
        teachers = db.query(Teacher).all()
        return [{"id": t.id, "full_name": t.full_name} for t in teachers]
    finally:
        db.close()

@app.post("/api/teachers/")
@allow_options
def add_teacher(data: EntityCreate):
    db = SessionLocal()
    try:
        if not data.full_name:
            raise HTTPException(status_code=400, detail="Teacher full name is required")
        teacher = Teacher(full_name=data.full_name)
        db.add(teacher)
        db.commit()
        db.refresh(teacher)
        return {"id": teacher.id, "full_name": teacher.full_name}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add teacher: {str(e)}")
    finally:
        db.close()

@app.delete("/api/teachers/{full_name}/")
@allow_options
def delete_teacher(full_name: str):
    db = SessionLocal()
    try:
        teacher = db.query(Teacher).filter_by(full_name=full_name).first()
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")
        db.delete(teacher)
        db.commit()
        return {"status": "ok"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete teacher: {str(e)}")
    finally:
        db.close()

# ==================== API: Schedule ====================
@app.get("/api/schedule/")
@allow_options
def get_schedule(week_start: str = Query(...), group_id: int = 1):
    db = SessionLocal()
    try:
        schedules = db.query(Schedule).all()
        result = []
        for s in schedules:
            result.append({
                "id": s.id,
                "row": s.day_of_week,
                "col": s.col,
                "subject": s.subject.name if s.subject else "",
                "room": s.classroom.number if s.classroom else "",
                "teacher": s.teacher.full_name if s.teacher else "",
            })
        return result
    finally:
        db.close()

@app.post("/api/schedule/")
@allow_options
def post_schedule(data: dict):
    db = SessionLocal()
    try:
        subject = db.query(Subject).filter_by(name=data.get("subject")).first()
        teacher = db.query(Teacher).filter_by(full_name=data.get("teacher")).first()
        room = db.query(Classroom).filter_by(number=data.get("room")).first()
        sched = Schedule(
            day_of_week=data.get("row"),
            col=data.get("col"),
            start_time="09:00",
            end_time="10:30",
            subject_id=subject.id if subject else None,
            teacher_id=teacher.id if teacher else None,
            classroom_id=room.id if room else None,
        )
        db.add(sched)
        db.commit()
        return {"status": "ok"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add schedule: {str(e)}")
    finally:
        db.close()

@app.delete("/api/schedule/")
@allow_options
def delete_schedule(week_start: str = Query(...), row: int = Query(...), col: int = Query(...)):
    db = SessionLocal()
    try:
        sched = db.query(Schedule).filter_by(day_of_week=row, col=col).first()
        if sched:
            db.delete(sched)
            db.commit()
        return {"status": "ok"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete schedule: {str(e)}")
    finally:
        db.close()