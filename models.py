from pydantic import BaseModel

class Question(BaseModel):
    category: str
    difficulty: str
    question_s: str
    answer: str