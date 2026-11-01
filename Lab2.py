from enum import Enum
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

# Перечень возможных значений по ключу completed_labs
class LabsChoices(Enum):
    Lab1 = 'LR1'
    Lab2 = 'LR2'
    Lab3 = 'LR3'

# Базовая схема студента
class Student(BaseModel):
    first_name: str
    second_name: str
    group: int
    completed_labs: list[LabsChoices]

# Схема с системным ID для ответа клиенту
class StudentWithID(Student):
    id: int

app = FastAPI(
    title="Labs API",
    description="Лабораторная работа №2: FastAPI, Pydantic, Swagger"
)

# Локальное хранилище данных в памяти
STUDENTS = [
    {'first_name': 'Алексей', 'second_name': 'Иванов', 'group': '507', 'completed_labs': ['LR1', 'LR2'], 'id': 1},
    {'first_name': 'Мария', 'second_name': 'Смирнова', 'group': '506', 'completed_labs': ['LR1', 'LR2', 'LR3'], 'id': 2},
    {'first_name': 'Дмитрий', 'second_name': 'Кузнецов', 'group': '506', 'completed_labs': ['LR1'], 'id': 3},
    {'first_name': 'Анна', 'second_name': 'Попова', 'group': '507', 'completed_labs': [], 'id': 4},
    {'first_name': 'Сергей', 'second_name': 'Васильев', 'group': '507', 'completed_labs': ['LR1', 'LR2', 'LR3'], 'id': 5}
]

# GET получение всего списка студентов
@app.get('/Students')
def students() -> list[StudentWithID]:
    return [
        StudentWithID(**s) for s in STUDENTS
    ]

# GET получение студента по ID
@app.get('/Students/{student_id}')
def student_with_id(student_id: int) -> StudentWithID:
    exact_student = next((StudentWithID(**s) for s in STUDENTS if s['id'] == student_id), None)
    return exact_student

# POST создание новой записи студента
@app.post('/Students')
def create_student(student_data: Student) -> StudentWithID:
    id = STUDENTS[-1]['id'] + 1
    student = StudentWithID(id=id, **student_data.model_dump()).model_dump()
    STUDENTS.append(student)
    return student

# DELETE удаление студента по ID
@app.delete('/Students/{student_id}')
def delete_student(student_id: int):
    exact_student = next((s for s in STUDENTS if s['id'] == student_id), None)
    if exact_student is None:
        raise HTTPException(status_code=404, detail=f'Student with ID {student_id} not found')
    STUDENTS.remove(exact_student)
    return None