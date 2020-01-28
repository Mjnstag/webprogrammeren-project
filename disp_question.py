from cs50 import SQL
import time
import random

db = SQL("sqlite:///sessions.db")

def question(gamemode, uuid, correct_answered):
    time.sleep(1)
    if gamemode == "custom":
        # send question data to page
        question = db.execute("SELECT question FROM customgame WHERE uuid = :uuid",
        uuid = uuid)
        if not question:
            return False
        answers = db.execute("SELECT correct, incorrect1, incorrect2, incorrect3 FROM customgame WHERE uuid = :uuid",
        uuid = uuid)

        answerlist = []
        answerlist.append(answers[0]["correct"])
        answerlist.append(answers[0]["incorrect1"])
        answerlist.append(answers[0]["incorrect2"])
        answerlist.append(answers[0]["incorrect3"])
        random.shuffle(answerlist)
        correct_answer = db.execute("SELECT correct FROM customgame WHERE uuid = :uuid",
        uuid = uuid)

        progress = db.execute("SELECT question_num FROM customgame WHERE uuid = :uuid",
        uuid = uuid)
        correct_answer = correct_answer[0]["correct"]
        return [progress, correct_answered, question, answerlist, correct_answer]

    # send question data to page
    question = db.execute("SELECT question FROM sp_questions WHERE uuid = :uuid",
    uuid = uuid)
    if not question:
        return False
    answers = db.execute("SELECT correct, incorrect1, incorrect2, incorrect3 FROM sp_questions WHERE uuid = :uuid",
    uuid = uuid)

    answerlist = []
    answerlist.append(answers[0]["correct"])
    answerlist.append(answers[0]["incorrect1"])
    answerlist.append(answers[0]["incorrect2"])
    answerlist.append(answers[0]["incorrect3"])
    random.shuffle(answerlist)
    correct_answer = db.execute("SELECT correct FROM sp_questions WHERE uuid = :uuid",
    uuid = uuid)

    progress = db.execute("SELECT question_num FROM sp_questions WHERE uuid = :uuid",
    uuid = uuid)
    correct_answer = correct_answer[0]["correct"]
    return [progress, correct_answered, question, answerlist, correct_answer]