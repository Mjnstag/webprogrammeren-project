import os

from cs50 import SQL
from flask import Flask
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import requests
import uuid
import time
import random

# configure flask
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQL("sqlite:///sessions.db")

# set default route
@app.route('/', defaults={'path': 'homepage'})
def catch_all(path):

    session["correct"] = None
    session["id"] = str(uuid.uuid4())
    return render_template(path + '.html')

# renders gamerules page
@app.route("/gamerules", methods=["GET", "POST"])
def show_rules():
    return render_template("gamerules.html")


@app.route("/question", methods=["GET", "POST"])
def disp_question():

    if request.method == 'POST':

        # render page
        return render_template('question.html')
    else:
        time.sleep(1)

        # send question data to page
        question = db.execute("SELECT question FROM sp_questions WHERE uuid = :uuid",
        uuid = session["id"])
        if not question:
            return redirect("/highscore_sp")
        answers = db.execute("SELECT correct, incorrect1, incorrect2, incorrect3 FROM sp_questions WHERE uuid = :uuid",
        uuid = session["id"])

        answerlist = []
        answerlist.append(answers[0]["correct"])
        answerlist.append(answers[0]["incorrect1"])
        answerlist.append(answers[0]["incorrect2"])
        answerlist.append(answers[0]["incorrect3"])
        random.shuffle(answerlist)
        correct_answer = db.execute("SELECT correct FROM sp_questions WHERE uuid = :uuid",
        uuid = session["id"])
        correct_answer = correct_answer[0]["correct"]
        return render_template('question.html', answered = session["correct"], question = question, answers = answerlist, correct_answer = correct_answer)


# renders categories page or redirects to next page
@app.route("/categories", methods=["GET", "POST"])
def categories():
    if request.method == 'POST':
        session['category'] = request.form["Categories"]
        session['difficulty'] = request.form["Difficulty"]
        return redirect('type_game')
    return render_template("categories.html")


# renders game type page
@app.route("/type_game")
def type_game():
    return render_template("type_game.html")


# resets correct score, renders singleplayer page, redirect to question
@app.route("/singleplayer", methods=["GET", "POST"])
def singleplayer():
    if request.method == "POST":
        session["correct"] = 0

        # makes sure to redirect to right high score database later
        session["gamemode"] = "standard"
        return redirect("/question")
    session["correct"] = 0
    session["gamemode"] = "standard"



    return render_template("singleplayer.html")


@app.route("/joinmp", methods=["GET", "POST"])
def joinmp():
    if request.method == "POST":

        room_id = request.form["roomid"]
        session['room_id'] = room_id
        username = request.form["username"]

        if not db.execute("SELECT room_id FROM mp_question WHERE room_id = :room_id", room_id = room_id):
            return render_template("joinmp.html", error = "Room does not exists")

        elif db.execute("SELECT username FROM mp_players WHERE username = :username", username = username):
            return render_template("joinmp.html", error = "Username is already being used in this room")


        db.execute("INSERT INTO mp_players (uuid, room_id, username, score, host) VALUES (:uuid, :room_id, :username, :score, :host)",
        uuid = session['id'],
        room_id = request.form.get("roomid"),
        username = request.form.get("username"),
        score = 0,
        host = 0)

        return redirect("/highscore_mp")
    return render_template("joinmp.html")

@app.route("/createmp", methods=["GET", "POST"])
def createmp():
    if request.method == "POST":
        from mp_question import get_question
        room_id = request.form["room_id"]
        session['room_id'] = room_id

        if db.execute("SELECT question FROM mp_question WHERE room_id = :room_id", room_id = room_id):
            return render_template("createmp.html", error = "Room already exists")


        db.execute("INSERT INTO mp_players (uuid, room_id, username, score, host) VALUES (:uuid, :room_id, :username, :score, :host)",
        uuid = session['id'],
        room_id = request.form.get("room_id"),
        username = request.form.get("username"),
        score = 0,
        host = 1)

        get_question(room_id, session['category'], session['difficulty'])
        return redirect("/highscore_mp")
    return render_template("createmp.html")



@app.route("/customgame", methods=["GET", "POST"])
def rendercustomgame():


    if request.method == "POST":
        session["correct"] = 0
        session["gamemode"] = "custom"
        return redirect("/question")
    session["correct"] = 0
    session["gamemode"] = "custom"
    return render_template("customgame.html")

@app.route("/customgamequestions", methods=["GET", "POST"])
def customgame():
    from customgame import get_question

    session['username'] = str(request.args.get("username", ""))
    user_id = str(session["id"])
    category = session['category']
    difficulty = session['difficulty']
    session["amount"] = str(request.args.get("amount", ""))

    get_question(user_id, session['username'], category, difficulty, session["amount"])
    return jsonify(True)
@app.route("/highscore_sp")
def highscore_sp():



    amount = session["amount"]
    uuid = session["id"]
    username =  session['username']
    score = session['correct']
    category = session['category']


    # checks if user is already in database, and only updates when the new score is higher than the existing score

    print("gamemode")
    if session["gamemode"] == "custom":

        scoreindatabase = db.execute("SELECT score from custom_highscore WHERE username = :username AND amount = :amount",
        username =  username,
        amount = amount)

        highscoredata = db.execute("SELECT * FROM custom_highscore  WHERE amount = :amount ORDER BY score DESC",
        amount = amount)
        highscoretext = "Congratulations! You made it into the high scores!"
        highscores = db.execute("SELECT score FROM custom_highscore WHERE amount = :amount ORDER BY score ASC",
        amount = amount)
        highscoresnames = db.execute("SELECT username FROM custom_highscore WHERE amount = :amount ORDER BY score ASC",
        amount = amount)

        if not highscoredata:

            db.execute("INSERT INTO custom_highscore (uuid, username, score, category, amount) VALUES (:uuid, :username, :score, :category, :amount)",
            uuid = uuid,
            username = username,
            score = score,
            category = category,
            amount = amount)
            highscoredata = db.execute("SELECT * FROM custom_highscore WHERE amount = :amount ORDER BY score DESC",
            amount = amount)
            return render_template("highscore_sp.html", score = score, username = username,
                category = category, amount = amount, highscoretext = highscoretext, highscoredata = highscoredata)

            # if number of high scores is less than 10, add high score
        elif len(highscoredata) < 10:
            if not scoreindatabase:
                db.execute("INSERT INTO custom_highscore (uuid, username, score, category, amount) VALUES (:uuid, :username, :score, :category, :amount)",
                uuid = uuid,
                username = username,
                score = score,
                category = category,
                amount = amount)
                highscoredata = db.execute("SELECT * FROM custom_highscore WHERE amount = :amount ORDER BY score DESC",
                amount = amount)
                return render_template("highscore_sp.html", score = score, username = username,
                        category = category, amount = amount, highscoretext = highscoretext, highscoredata = highscoredata)

            else:
                if session['correct'] > scoreindatabase[0]["score"]:
                    db.execute("UPDATE custom_highscore SET score = :score, category = :category, amount = :amount WHERE username = :username",
                    score = score,
                    category = category,
                    username = username,
                    amount = amount)

                    highscoredata = db.execute("SELECT * FROM sp_highscore WHERE amount = :amount ORDER BY score DESC",
                    category = category)
                    return render_template("highscore_sp.html", score = score, username = username,
                    category = category, amount = amount, highscoretext = highscoretext, highscoredata = highscoredata)

                return render_template("highscore_sp.html", highscoredata = highscoredata, score = score, amount = amount)
        else:

            # adds user to high score database
            if not scoreindatabase:
                db.execute("INSERT INTO custom_highscore (uuid, username, score, category, amount) VALUES (:uuid, :username, :score, :category, :amount)",
                uuid = uuid,
                username = username,
                score = score,
                category = category,
                amount = amount)


                db.execute("DELETE FROM custom_highscore WHERE score = :score AND username = :username",
                score = highscores[0]["score"],
                username = highscoresnames[0]["username"],
                amount = amount)



                highscoredata = db.execute("SELECT * FROM custom_highscore WHERE amount = :amount ORDER BY score DESC",
                category = category,
                amount = amount)

                return render_template("highscore_sp.html", score = score, username = username,
                    category = category, amount = amount, highscoretext = highscoretext, highscoredata = highscoredata)

                # else updates highscore
            else:
                if session['correct'] > scoreindatabase[0]["score"]:
                    db.execute("UPDATE custom_highscore SET score = :score, category = :category WHERE username = :username",
                    score = score,
                    category = category,
                    username = username,
                    amount = amount)
                    highscoredata = db.execute("SELECT * FROM sp_highscore WHERE amount = :amount ORDER BY score DESC",
                    category = category)
                    return render_template("highscore_sp.html", score = score, username = username,
                    category = category, amount = amount, highscoretext = highscoretext, highscoredata = highscoredata)

                return render_template("highscore_sp.html", amount = amount, highscoredata = highscoredata, score = score)

        return render_template("custom_highscore", amount = amount, highscoredata = highscoredata, score = score)



    scoreindatabase = db.execute("SELECT score from sp_highscore WHERE username = :username AND category = :category",
    username =  username,
    category = category)

    highscoredata = db.execute("SELECT * FROM sp_highscore WHERE category = :category ORDER BY score DESC",
    category = category)
    highscoretext = "Congratulations! You made it into the high scores!"
    highscores = db.execute("SELECT score FROM sp_highscore WHERE category = :category ORDER BY score ASC",
    category = category)
    highscoresnames = db.execute("SELECT username FROM custom_highscore WHERE category = :category ORDER BY score ASC",
    category = category)

    # checks if highscore list is empty
    if not highscoredata:

        db.execute("INSERT INTO sp_highscore (uuid, username, score, category) VALUES (:uuid, :username, :score, :category)",
        uuid = uuid,
        username = username,
        score = score,
        category = category)
        highscoredata = db.execute("SELECT * FROM sp_highscore WHERE category = :category ORDER BY score DESC",
        category = session['category'])
        return render_template("highscore_sp.html", score = score, username = username,
            category = category, highscoretext = highscoretext, highscoredata = highscoredata)

    # if number of high scores is less than 10, add high score
    elif len(highscoredata) < 10:
        if not scoreindatabase:
            db.execute("INSERT INTO sp_highscore (uuid, username, score, category) VALUES (:uuid, :username, :score, :category)",
            uuid = uuid,
            username = username,
            score = score,
            category = category)
            highscoredata = db.execute("SELECT * FROM sp_highscore WHERE category = :category ORDER BY score DESC",
            category = session['category'])
            return render_template("highscore_sp.html", score = score, username = username,
                category = category, highscoretext = highscoretext, highscoredata = highscoredata)

        else:
            if session['correct'] > scoreindatabase[0]["score"]:
                db.execute("UPDATE sp_highscore SET score = :score, category = :category WHERE username = :username",
                score = score,
                category = category,
                username = username)

                highscoredata = db.execute("SELECT * FROM sp_highscore WHERE category = :category ORDER BY score DESC",
                category = category)
                return render_template("highscore_sp.html", score = score, username = username,
                category = category, highscoretext = highscoretext, highscoredata = highscoredata)

            return render_template("highscore_sp.html", highscoredata = highscoredata, score = score)
    else:

        # adds user to high score database
        if not scoreindatabase:
            db.execute("INSERT INTO sp_highscore (uuid, username, score, category) VALUES (:uuid, :username, :score, :category)",
            uuid = uuid,
            username = username,
            score = score,
            category = category)


            db.execute("DELETE FROM sp_highscore WHERE score = :score AND username = :username",
            score = highscores[0]["score"],
            username = highscoresnames[0]["username"])


            highscoredata = db.execute("SELECT * FROM sp_highscore WHERE category = :category ORDER BY score DESC",
            category = category)

            return render_template("highscore_sp.html", score = score, username = username,
                category = category, highscoretext = highscoretext, highscoredata = highscoredata)

        # else updates highscore
        else:
            if session['correct'] > scoreindatabase[0]["score"]:
                db.execute("UPDATE sp_highscore SET score = :score, category = :category WHERE username = :username",
                score = score,
                category = category,
                username = username)
                highscoredata = db.execute("SELECT * FROM sp_highscore WHERE category = :category ORDER BY score DESC",
                category = category)
                return render_template("highscore_sp.html", score = score, username = username,
                category = category, highscoretext = highscoretext, highscoredata = highscoredata)

            return render_template("highscore_sp.html", highscoredata = highscoredata, score = score)

    return render_template("highscore_sp.html", highscoredata = highscoredata, score = score)

@app.route("/highscore_mp")
def highscore_mp():
    data = db.execute("SELECT * FROM mp_players WHERE room_id = :room_id", room_id=session['room_id'])
    return render_template("highscore_mp.html", data = data)

# calls on function to put questions in database
@app.route("/sp_question", methods=["GET", "POST"])
def sp_question():
    # import function from .py file
    from sp_question import get_question

    # get needed variables
    session['username'] = str(request.args.get("username", ""))
    user_id = str(session["id"])
    category = session['category']
    difficulty = session['difficulty']

    # call function to add questions in database
    get_question(user_id, session['username'],  category, difficulty)

    # return
    return jsonify(True)


# checks and handles answers and time-outs for questions
@app.route("/correct", methods=["GET", "POST"])
def correct():
    # if answer is correct, add score point
    if request.args.get("data", "") == request.args.get("answer", ""):
        session["correct"] += 1

    # delete question from sp_question db
    db.execute("DELETE FROM sp_questions WHERE correct = :correct AND uuid = :session_id", correct = request.args.get("data", ""), session_id = session['id'])
    return jsonify(True)
