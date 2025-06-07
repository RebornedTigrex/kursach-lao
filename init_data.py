from sqlalchemy.orm import Session
from models import SessionLocal, Faculty, Department, Group, Subject, Teacher, Classroom, Schedule
from datetime import time

def init_sample_data():
    db = SessionLocal()
    
    try:
        # Факультеты
        faculty = Faculty(name="Факультет информационных технологий")
        db.add(faculty)
        db.commit()
        
        # Кафедры
        dept1 = Department(name="Кафедра программирования", faculty_id=faculty.id)
        dept2 = Department(name="Кафедра математики", faculty_id=faculty.id)
        db.add_all([dept1, dept2])
        db.commit()
        
        # Группы
        group1 = Group(name="ИТ-101", department_id=dept1.id)
        group2 = Group(name="ИТ-102", department_id=dept1.id)
        db.add_all([group1, group2])
        db.commit()
        
        # Предметы
        subjects = [
            Subject(name="Программирование на Python"),
            Subject(name="Базы данных"),
            Subject(name="Алгоритмы и структуры данных"),
            Subject(name="Математический анализ"),
            Subject(name="Линейная алгебра"),
        ]
        db.add_all(subjects)
        db.commit()
        
        # Преподаватели
        teachers = [
            Teacher(full_name="Иванов Иван Иванович"),
            Teacher(full_name="Петрова Мария Сергеевна"),
            Teacher(full_name="Сидоров Алексей Владимирович"),
        ]
        # Назначаем преподавателям предметы
        teachers[0].subjects = [subjects[0], subjects[2]]  # Иванов ведет Python и Алгоритмы
        teachers[1].subjects = [subjects[1]]              # Петрова ведет Базы данных
        teachers[2].subjects = [subjects[3], subjects[4]] # Сидоров ведет Матан и Линал
        db.add_all(teachers)
        db.commit()
        
        # Аудитории
        classrooms = [
            Classroom(number="101", building="Главный корпус", capacity=30),
            Classroom(number="304", building="Главный корпус", capacity=25),
            Classroom(number="201", building="2 корпус", capacity=40),
        ]
        db.add_all(classrooms)
        db.commit()
        
        # Расписание
        schedules = [
            Schedule(
                day_of_week=0,  # Понедельник
                start_time=time(9, 0),
                end_time=time(10, 30),
                group_id=group1.id,
                subject_id=subjects[0].id,
                teacher_id=teachers[0].id,
                classroom_id=classrooms[0].id
            ),
            Schedule(
                day_of_week=2,  # Среда
                start_time=time(10, 40),
                end_time=time(12, 10),
                group_id=group1.id,
                subject_id=subjects[2].id,
                teacher_id=teachers[0].id,
                classroom_id=classrooms[1].id
            ),
            # Добавьте другие занятия по аналогии
        ]
        db.add_all(schedules)
        db.commit()
        
        print("Sample data initialized successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error initializing sample data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_sample_data()