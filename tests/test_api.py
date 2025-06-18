import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi.testclient import TestClient
from core.api import app, SessionLocal, Subject, Teacher, Classroom, Schedule
import json

client = TestClient(app)

def setup_module(module):
    # Очистка базы перед тестами
    db = SessionLocal()
    db.query(Schedule).delete()
    db.query(Subject).delete()
    db.query(Teacher).delete()
    db.query(Classroom).delete()
    db.commit()
    db.close()

def test_subjects_crud():
    # Добавление предмета
    r = client.post("/api/subjects/", json="Математика")
    assert r.status_code == 200
    subject_id = r.json()["id"]
    # Получение предметов
    r = client.get("/api/subjects/")
    assert r.status_code == 200
    assert any(s["name"] == "Математика" for s in r.json())
    # Удаление предмета
    r = client.request(
        "DELETE",
        "/api/subjects/",
        json=subject_id
    )
    assert r.status_code == 200

def test_rooms_crud():
    r = client.post("/api/rooms/", json="101")
    assert r.status_code == 200
    room_id = r.json()["id"]
    r = client.get("/api/rooms/")
    assert r.status_code == 200
    assert any(rm["number"] == "101" for rm in r.json())
    r = client.request(
        "DELETE",
        "/api/rooms/",
        json=room_id
    )
    assert r.status_code == 200

def test_teachers_crud():
    r = client.post("/api/teachers/", json="Иванов И.И.")
    assert r.status_code == 200
    teacher_id = r.json()["id"]
    r = client.get("/api/teachers/")
    assert r.status_code == 200
    assert any(t["full_name"] == "Иванов И.И." for t in r.json())
    r = client.request(
        "DELETE",
        "/api/teachers/",
        json=teacher_id
    )
    assert r.status_code == 200

def test_schedule_crud():
    # Добавим сущности
    subj = client.post("/api/subjects/", json="Физика").json()["id"]
    room = client.post("/api/rooms/", json="202").json()["id"]
    teacher = client.post("/api/teachers/", json="Петров П.П.").json()["id"]
    # Добавим расписание
    key = "2025-06-16_1_2"
    data = {
        key: {
            "subject": "Физика",
            "room": "202",
            "teacher": "Петров П.П."
        }
    }
    r = client.post("/api/schedule/", json=data)
    assert r.status_code == 200
    # Проверим получение
    r = client.get("/api/schedule/")
    assert r.status_code == 200
    assert key in r.json()
    # Удалим расписание
    r = client.request(
        "DELETE",
        "/api/schedule/",
        json=key
    )
    assert r.status_code == 200
    # Очистим сущности
    client.request("DELETE", "/api/subjects/", json=subj)
    client.request("DELETE", "/api/rooms/", json=room)
    client.request("DELETE", "/api/teachers/", json=teacher)
