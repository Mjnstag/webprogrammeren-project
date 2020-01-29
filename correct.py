from cs50 import SQL


def check_correct(gamemode, correct, uuid):
    # configure database
    db = SQL("sqlite:///sessions.db")

    # delete question from sp_question database
    if gamemode == "standard":
        db.execute("DELETE FROM sp_questions WHERE correct = :correct AND uuid = :uuid", correct=correct, uuid=uuid)

    # delete question from customgame database
    elif gamemode == "custom":
        db.execute("DELETE FROM customgame WHERE correct = :correct AND uuid = :uuid", correct=correct, uuid=uuid)

    # return
    return None