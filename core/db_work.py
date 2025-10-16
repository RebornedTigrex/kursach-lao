from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind = engine)
Base = declarative_base()


def connect_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, unique = True, nullable = False)


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key = True, index = True)
    full_name = Column(String, nullable = False)


class Classroom(Base):
    __tablename__ = "classrooms"
    id = Column(Integer, primary_key = True, index = True)
    number = Column(String, nullable = False)


class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key = True, index = True)
    datekey = Column(String)
    dateMon = Column(Date, nullable = False)  # дата пары по понедельникам
    lesson_number = Column(Integer, nullable = False)  # номер пары (например, 3)
    day_of_week = Column(Integer, nullable = False)  # номер дня недели (например, 2)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    classroom_id = Column(Integer, ForeignKey("classrooms.id"))

    subject = relationship("Subject")
    teacher = relationship("Teacher")
    classroom = relationship("Classroom")


class Auth(Base):
    __tablename__ = "auth"
    id = Column(Integer, primary_key = True, index = True)
    user = Column(String, nullable = False, unique = True)
    password_hash = Column(String, nullable = False)
    email = Column(String)


# Создание таблиц

def init_db():
    Base.metadata.create_all(bind = engine)


__all__ = ["Subject", "Teacher", "Classroom", "Schedule", "Auth"]

if __name__ == "__main__":
    init_db()
