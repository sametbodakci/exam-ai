from pydantic import BaseModel
from typing import List, Optional

class QuestionBase(BaseModel):
    text: str

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    class Config:
        orm_mode = True

class ExamBase(BaseModel):
    title: str
    description: Optional[str] = None

class ExamCreate(ExamBase):
    questions: List[QuestionCreate] = []

class Exam(ExamBase):
    id: int
    questions: List[Question] = []
    class Config:
        orm_mode = True
