from sqlalchemy.orm import Session
from models import SessionLocal, Faculty, Department, Group, Subject, Teacher, Classroom, Schedule
from datetime import time

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DBActions:
    @staticmethod
    def create_faculty(db: Session, name: str):
        faculty = Faculty(name=name)
        db.add(faculty)
        db.commit()
        db.refresh(faculty)
        return faculty

    @staticmethod
    def create_department(db: Session, name: str, faculty_id: int):
        department = Department(name=name, faculty_id=faculty_id)
        db.add(department)
        db.commit()
        db.refresh(department)
        return department

    @staticmethod
    def create_group(db: Session, name: str, department_id: int):
        group = Group(name=name, department_id=department_id)
        db.add(group)
        db.commit()
        db.refresh(group)
        return group

    @staticmethod
    def create_subject(db: Session, name: str):
        subject = Subject(name=name)
        db.add(subject)
        db.commit()
        db.refresh(subject)
        return subject

    @staticmethod
    def create_teacher(db: Session, full_name: str, subject_ids: list[int] = None):
        teacher = Teacher(full_name=full_name)
        if subject_ids:
            subjects = db.query(Subject).filter(Subject.id.in_(subject_ids)).all()
            teacher.subjects.extend(subjects)
        db.add(teacher)
        db.commit()
        db.refresh(teacher)
        return teacher

    @staticmethod
    def create_classroom(db: Session, number: str, building: str = None, capacity: int = None):
        classroom = Classroom(number=number, building=building, capacity=capacity)
        db.add(classroom)
        db.commit()
        db.refresh(classroom)
        return classroom

    @staticmethod
    def create_schedule(
        db: Session,
        day_of_week: int,
        start_time: time,
        end_time: time,
        group_id: int,
        subject_id: int,
        teacher_id: int,
        classroom_id: int
    ):
        schedule = Schedule(
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            group_id=group_id,
            subject_id=subject_id,
            teacher_id=teacher_id,
            classroom_id=classroom_id
        )
        db.add(schedule)
        db.commit()
        db.refresh(schedule)
        return schedule

    @staticmethod
    def get_group_schedule(db: Session, group_id: int, week_offset: int = 0):
        # Здесь можно добавить логику для работы с неделями
        return db.query(Schedule).filter(Schedule.group_id == group_id).order_by(
            Schedule.day_of_week,
            Schedule.start_time
        ).all()

    @staticmethod
    def get_teacher_schedule(db: Session, teacher_id: int, week_offset: int = 0):
        return db.query(Schedule).filter(Schedule.teacher_id == teacher_id).order_by(
            Schedule.day_of_week,
            Schedule.start_time
        ).all()

    @staticmethod
    def get_classroom_schedule(db: Session, classroom_id: int, week_offset: int = 0):
        return db.query(Schedule).filter(Schedule.classroom_id == classroom_id).order_by(
            Schedule.day_of_week,
            Schedule.start_time
        ).all()