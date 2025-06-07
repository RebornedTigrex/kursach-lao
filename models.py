from datetime import time
from sqlalchemy import create_engine, Column, Integer, String, Time, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

# Ассоциативная таблица для связи многие-ко-многим между Subject и Teacher
subject_teacher_association = Table(
    'subject_teacher', Base.metadata,
    Column('subject_id', Integer, ForeignKey('subjects.id')),
    Column('teacher_id', Integer, ForeignKey('teachers.id'))
)

class Faculty(Base):
    __tablename__ = 'faculties'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    departments = relationship("Department", back_populates="faculty")

class Department(Base):
    __tablename__ = 'departments'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    faculty_id = Column(Integer, ForeignKey('faculties.id'))
    faculty = relationship("Faculty", back_populates="departments")
    groups = relationship("Group", back_populates="department")

class Group(Base):
    __tablename__ = 'groups'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))
    department = relationship("Department", back_populates="groups")
    schedules = relationship("Schedule", back_populates="group")

class Subject(Base):
    __tablename__ = 'subjects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    teachers = relationship("Teacher", secondary=subject_teacher_association, back_populates="subjects")
    schedules = relationship("Schedule", back_populates="subject")

class Teacher(Base):
    __tablename__ = 'teachers'
    
    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    subjects = relationship("Subject", secondary=subject_teacher_association, back_populates="teachers")
    schedules = relationship("Schedule", back_populates="teacher")

class Classroom(Base):
    __tablename__ = 'classrooms'
    
    id = Column(Integer, primary_key=True)
    number = Column(String(20), nullable=False)
    building = Column(String(20))
    capacity = Column(Integer)
    schedules = relationship("Schedule", back_populates="classroom")

class Schedule(Base):
    __tablename__ = 'schedules'
    
    id = Column(Integer, primary_key=True)
    day_of_week = Column(Integer, nullable=False)  # 0-6 (пн-вс)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship("Group", back_populates="schedules")
    
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    subject = relationship("Subject", back_populates="schedules")
    
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship("Teacher", back_populates="schedules")
    
    classroom_id = Column(Integer, ForeignKey('classrooms.id'))
    classroom = relationship("Classroom", back_populates="schedules")

# Создаем движок и подключаемся к БД
DATABASE_URL = "postgresql://username:password@localhost/schedule_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)