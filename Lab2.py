from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel

# Перечень возможных значений по ключу completed_labs
class LabsChoices(Enum):
    Lab1 = 'LR1'
    Lab2 = 'LR2'
    Lab3 = 'LR3'

class Student(BaseModel):
    id: int
    first_name: str
    second_name: str
    group: int
    completed_labs: [LabsChoices]

app = FastAPI(
    title="Labs API",
    description="Лабораторная работа №2: FastAPI, Pydantic, Swagger"
)

# Локальное хранилище данных в памяти
STUDENTS = [
    {'id': 1, 'first_name': 'Алексей', 'second_name': 'Иванов', 'group': '507', 'completed_labs': ['LR1', 'LR2']},
    {'id': 2, 'first_name': 'Мария', 'second_name': 'Смирнова', 'group': '506', 'completed_labs': ['LR1', 'LR2', 'LR3']},
    {'id': 3, 'first_name': 'Дмитрий', 'second_name': 'Кузнецов', 'group': '506', 'completed_labs': ['LR1']},
    {'id': 4, 'first_name': 'Анна', 'second_name': 'Попова', 'group': '507', 'completed_labs': []},
    {'id': 5, 'first_name': 'Сергей', 'second_name': 'Васильев', 'group': '507', 'completed_labs': ['LR1', 'LR2', 'LR3']}
]