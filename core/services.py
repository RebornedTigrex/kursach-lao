from fastapi import Body, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any
import re

from core.db_work import *
from core.auth import register_user, authenticate_user


def s_get_subjects(db: Session):
    subjects = db.query(Subject).all()
    return [{"id": s.id, "name": s.name} for s in subjects]


def s_get_rooms(db: Session):
    rooms = db.query(Classroom).all()
    return [{"id": r.id, "number": r.number} for r in rooms]


def s_get_teachers(db: Session):
    teachers = db.query(Teacher).all()
    return [{"id": t.id, "full_name": t.full_name} for t in teachers]


def s_get_schedule(db: Session):
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


def s_post_schedule(db: Session, current_user: dict[str, Any], data: dict):
    print(f"for test and logs: это сделаль этот шушпин: {current_user['username']}, с id = {current_user['id']}")
    print(data)
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
        subject = db.query(Subject).filter_by(name = value.get("subject")).first()
        teacher = db.query(Teacher).filter_by(full_name = value.get("teacher")).first()
        room = db.query(Classroom).filter_by(number = value.get("room")).first()
        sched = Schedule(
            datekey = datekey,
            dateMon = date_obj,
            lesson_number = lesson_number,
            day_of_week = day_of_week,
            subject_id = subject.id if subject else None,
            teacher_id = teacher.id if teacher else None,
            classroom_id = room.id if room else None,
        )
        db.add(sched)
    db.commit()
    return {"status": "ok"}


def s_delete_schedule(db: Session, current_user: dict[str, Any], key: str = Body(...)):
    print(f"for test and logs: это сделаль этот шушпин: {current_user['username']}, с id = {current_user['id']}")
    sched = db.query(Schedule).filter_by(datekey = key).first()
    if sched:
        db.delete(sched)
        db.commit()
        return {"status": "ok"}
    else:
        return {"status": "error", "msg": "invalid key"}


def s_post_subject(db: Session, current_user: dict[str, Any], data: str = Body(...)):
    print(f"for test and logs: это сделаль этот шушпин: {current_user['username']}, с id = {current_user['id']}")
    name = data
    if not name:
        return {"status": "error", "msg": "name required"}
    subject = Subject(name = name)
    db.add(subject)
    db.commit()
    return {"status": "ok", "id": subject.id}


def s_delete_subject(db: Session, current_user: dict[str, Any], id: int = Body(...)):
    print(f"for test and logs: это сделаль этот шушпин: {current_user['username']}, с id = {current_user['id']}")
    subject = db.query(Subject).filter_by(id = id).first()
    if subject:
        db.delete(subject)
        db.commit()
    return {"status": "ok"}


def s_post_room(db: Session, current_user: dict[str, Any], data: str = Body(...)):
    print(f"for test and logs: это сделаль этот шушпин: {current_user['username']}, с id = {current_user['id']}")
    number = data
    if not number:
        return {"status": "error", "msg": "number required"}
    room = Classroom(number = number)
    db.add(room)
    db.commit()
    return {"status": "ok", "id": room.id}


def s_delete_room(db: Session, current_user: dict[str, Any], id: int = Body(...)):
    print(f"for test and logs: это сделаль этот шушпин: {current_user['username']}, с id = {current_user['id']}")
    print(f"Deleting room with id: {id}")
    room = db.query(Classroom).filter_by(id = id).first()
    if room:
        db.delete(room)
        db.commit()
    return {"status": "ok"}


def s_post_teacher(db: Session, current_user: dict[str, Any], data: str = Body(...)):
    print(f"for test and logs: это сделаль этот шушпин: {current_user['username']}, с id = {current_user['id']}")
    full_name = data
    if not full_name:
        return {"status": "error", "msg": "full_name required"}
    teacher = Teacher(full_name = full_name)
    db.add(teacher)
    db.commit()
    return {"status": "ok", "id": teacher.id}


def s_delete_teacher(db: Session, current_user: dict[str, Any], id: int = Body(...)):
    print(f"for test and logs: это сделаль этот шушпин: {current_user['username']}, с id = {current_user['id']}")
    teacher = db.query(Teacher).filter_by(id = id).first()
    if teacher:
        db.delete(teacher)
        db.commit()
    return {"status": "ok"}


def _extract_credentials(data: Dict[str, Any]) -> tuple[str, str]:
    """
    Вспомогательная: извлечь username и password из data, валидировать минимум.
    Бросает HTTPException(400) если некорректно.
    :return: (username, password)
    """
    username = data.get("username", None)
    password = data.get("password", None)
    if not username or not password or not isinstance(password, str) or not isinstance(username, str):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Missing username or password")
    username = username.strip()
    reg = re.compile(r"\A([a-zA-Z0-9_-]){1,15}\Z")
    if not re.fullmatch(reg, username) or not re.fullmatch(reg, password):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Invalid username or password")

    return username, password


def s_post_register(db: Session, data: Dict[str, Any] = Body(...)) -> Dict[str, str]:
    """
    Сервис для регистрации: создаёт пользователя и возвращает access token.
    :param data: {"username": "...", "password": "..."}
    :return: возвращает access token в виде: {"access_token": str, "token_type": "bearer"}
    """
    username, password = _extract_credentials(data)

    token, _ = register_user(db, username, password)
    return {"access_token": token, "token_type": "bearer"}


def s_post_auth(db: Session, data: Dict[str, Any] = Body(...)) -> Dict[str, str]:
    """
    Сервис для аутентификации: проверяет логин/пароль
    :return: возвращает access token в виде: {"access_token": str, "token_type": "bearer"}
    """
    username, password = _extract_credentials(data)

    token = authenticate_user(db, username, password)
    return {"access_token": token, "token_type": "bearer"}

__all__ = ["s_get_subjects", "s_get_rooms", "s_get_teachers", "s_get_schedule", "s_post_schedule", "s_delete_schedule",
           "s_post_subject", "s_delete_subject", "s_post_room", "s_delete_room", "s_post_teacher", "s_delete_teacher",
           "s_post_register", "s_post_auth"]
