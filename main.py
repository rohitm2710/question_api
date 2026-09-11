from fastapi import FastAPI
import models
import sqlite3

app = FastAPI()

db = "question.db"

def init_mcq():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mcq(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            difficulty TEXT NOT NULL,
            question VARCHAR,
            option_a VARCHAR,
            option_b VARCHAR,
            option_c VARCHAR,
            option_d VARCHAR,
            answer TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.get("/questions")
def get_all_questions():
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mcq")

    all_questions = cursor.fetchall()

    conn.close()
    return all_questions

@app.post("/mcq")
def add_mcq(ques : models.mcq):
    init_mcq()
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(
        '''
            INSERT INTO mcq (difficulty,question, option_a, option_b, option_c, option_d,answer)
            VALUES (?,?, ?, ?, ?, ?, ?)
        ''',
        (ques.difficulty,ques.question, ques.option_a, ques.option_b, ques.option_c, ques.option_d, ques.answer)
    )
    conn.commit()

    ques_num = cursor.lastrowid

    conn.close()

    return {
        "message" : "Question succesfully added",
        "number" : ques_num
    }
