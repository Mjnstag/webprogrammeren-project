from cs50 import SQL
import time
import random

db = SQL("sqlite:///sessions.db")


def question(gamemode, uuid, correct_answered):
    time.sleep(1)

    if gamemode == "custom":
        # save question
        question = db.execute("SELECT question FROM customgame WHERE uuid = :uuid",
                              uuid=uuid)

        # if there are no remaining
        if not question:
            # return false
            return False

        # save answer data
        answers = db.execute("SELECT correct, incorrect1, incorrect2, incorrect3 FROM customgame WHERE uuid = :uuid",
                             uuid=uuid)

        # add current answers to list
        # kunnen we niet gewoon 'random.shuffle(answers[0])' doen?
        answerlist = []
        answerlist.append(answers[0]["correct"])
        answerlist.append(answers[0]["incorrect1"])
        answerlist.append(answers[0]["incorrect2"])
        answerlist.append(answers[0]["incorrect3"])
        # shuffle answers
        random.shuffle(answerlist)

        # save correct answer
        correct_answer = db.execute("SELECT correct FROM customgame WHERE uuid = :uuid",
                                    uuid=uuid)[0]['correct']
        # save question progress
        progress = db.execute("SELECT question_num FROM customgame WHERE uuid = :uuid",
                              uuid=uuid)

        # return question data
        return [progress, correct_answered, question, answerlist, correct_answer]

    # for classic game mode
    # save question
    question = db.execute("SELECT question FROM sp_questions WHERE uuid = :uuid",
                          uuid=uuid)
    # if there are no remainging
    if not question:
        # return false
        return False

    # save answer data
    answers = db.execute("SELECT correct, incorrect1, incorrect2, incorrect3 FROM sp_questions WHERE uuid = :uuid",
                         uuid=uuid)

    # append answerdata to list
    answerlist = []
    answerlist.append(answers[0]["correct"])
    answerlist.append(answers[0]["incorrect1"])
    answerlist.append(answers[0]["incorrect2"])
    answerlist.append(answers[0]["incorrect3"])
    # shuffle asnwer data
    random.shuffle(answerlist)

    # save correct answer
    correct_answer = db.execute("SELECT correct FROM sp_questions WHERE uuid = :uuid",
                                uuid=uuid)[0]["correct"]

    # save question progress
    progress = db.execute("SELECT question_num FROM sp_questions WHERE uuid = :uuid",
                          uuid=uuid)
    # return question data
    return [progress, correct_answered, question, answerlist, correct_answer]