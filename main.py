from fastapi import FastAPI
import models
import sqlite3

app = FastAPI()

db = "question.db"

@app.get("/")
def greet():
    return "hello"

@app.get("/questions")
def get_all_questions():
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions")

    all_questions = cursor.fetchall()

    conn.close()
    return all_questions

def init_db():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            question_s TEXT NOT NULL,
            answer TEXT NOT NULL
        )
''')
    conn.commit()
    conn.close()

init_db()

@app.post("/questions")
def add_question(question : models.Question):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO questions (category, difficulty, question_s, answer)
        VALUES (?, ?, ?, ?)
    ''',
    (question.category, question.difficulty, question.question_s, question.answer)
    )
    conn.commit()
    new_user_id = cursor.lastrowid

    conn.close()

    return {
        "message" : "Question saved successfully",
        "id" : new_user_id,
    }