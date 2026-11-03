from enum import Enum
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, JSON, select
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# Настройка БД ((SQLite и SQLAlchemy))
DATABASE_URL = "sqlite:///./students.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модель таблицы в БД
class StudentModel(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    group = Column(Integer, nullable=False)
    # Хранение списка в формате JSON
    completed_labs = Column(JSON, default=[])

# Создание таблиц при запуске
Base.metadata.create_all(bind=engine)

# Генератор сессий БД для внедрения зависимостей
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
    completed_labs: list[LabsChoices] = []

# Схема с системным ID для ответа клиенту
class StudentWithID(Student):
    id: int

app = FastAPI(
    title="Labs API",
    description="Лабораторная работа №3: ЛР2 + SQLite, SQLAlchemy"
)

# GET получение всего списка студентов
@app.get('/Students')
def students(db: Session = Depends(get_db)) -> list[StudentWithID]:
    query = select(StudentModel)
    return db.scalars(query).all()

# GET получение студента по ID
@app.get('/Students/{student_id}')
def student_with_id(student_id: int, db: Session = Depends(get_db)) -> StudentWithID:
    exact_student = db.get(StudentModel, student_id)
    if exact_student is None:
        raise HTTPException(status_code=404, detail=f'Student with ID {student_id} not found')
    return exact_student

# POST создание новой записи студента
@app.post('/Students')
def create_student(student_data: Student, db: Session = Depends(get_db)) -> StudentWithID:
    # Преобразуем Enum в строковые значения для JSON
    data = student_data.model_dump()
    data['completed_labs'] = [l.value for l in student_data.completed_labs]
    # Добавляем в БД
    db_student = StudentModel(**data)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# DELETE удаление студента по ID
@app.delete('/Students/{student_id}')
def delete_student(student_id: int, db: Session = Depends(get_db)):
    exact_student = db.get(StudentModel, student_id)
    if exact_student is None:
        raise HTTPException(status_code=404, detail=f'Student with ID {student_id} not found')
    db.delete(db_student)
    db.commit()
    return None
