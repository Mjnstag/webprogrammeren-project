import os

from cs50 import SQL
from flask import Flask
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import requests
import uuid
import time
import random

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQL("sqlite:///sessions.db")

@app.route('/', defaults={'path': 'homepage'})
# @app.route('/<path:path>')
def catch_all(path):
    session["id"] = str(uuid.uuid4())
    return render_template(path + '.html')

@app.route("/gamerules", methods=["GET", "POST"])
def show_rules():
    return render_template("gamerules.html")


@app.route("/question", methods=["GET", "POST"])
def disp_question():

    if request.method == 'POST':
        # render page
        return render_template('question.html')
    else:
        # import question.py
        from question import get_question

        # get question data
        question, answers, correct_answer = get_question(session['category'], session['difficulty'])

        # send question data to page
        question = db.execute("SELECT question FROM sp_questions WHERE uuid = :uuid",
        uuid = session["id"])
        print(question)
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


        #db.execute("DELETE FROM sp_questions WHERE question_num = 1")
        return render_template('question.html', answered = session["correct"], question = question, answers = answerlist, correct_answer = correct_answer)


@app.route("/categories", methods=["GET", "POST"])
def categories():
    # print(requests.get("https://opentdb.com/api_category.php").json()['trivia_categories'])
    if request.method == 'POST':
        session['category'] = request.form["Categories"]
        session['difficulty'] = request.form["Difficulty"]
        # print(session['category'])
        # print(session['difficulty'])
        return redirect('type_game')
    return render_template("categories.html")


@app.route("/type_game")
def type_game():
    if request.method == "POST":
        print("test")

        return render_template("type_game.html")
    return render_template("type_game.html")


@app.route("/singleplayer", methods=["GET", "POST"])
def singleplayer():
    if request.method == "POST":
        session["correct"] = 0
        return redirect("/question")
        # return render_template("singleplayer.html")
    session["correct"] = 0
    return render_template("singleplayer.html")


@app.route("/joinmp", methods=["GET", "POST"])
def joinmp():
    if request.method == "POST":
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

@app.route("/highscore_sp")
def highscore_sp():
    print(session["correct"])
    # insert user data
    # select top for highscores
    # send top to page


    # Checks if user is already in database, and only updates when the new score is higher than the existing score
    # hij checkt nu ook de username, kunnen we nog aanpassen
    scoreindatabase = db.execute("SELECT score from sp_highscore WHERE username = :username",
    username =  session['username'])

    highscoredata = db.execute("SELECT * FROM sp_highscore ORDER BY score DESC")
    highscoretext = "Congratulations! You made it into the high scores!"
    highscores = db.execute("SELECT score FROM sp_highscore ORDER BY score ASC")
    highscoresnames = db.execute("SELECT username FROM sp_highscore ORDER BY score ASC")
    print(highscoresnames)
    # Checks if highscore list is empty
    if not highscoredata:


        # Adds user to high score database
        if not scoreindatabase:
            db.execute("INSERT INTO sp_highscore (uuid, username, score, category) VALUES (:uuid, :username, :score, :category)",
            uuid = session["id"],
            username =  session['username'],
            score = session['correct'],
            category = session['category'])
            highscoredata = db.execute("SELECT * FROM sp_highscore ORDER BY score DESC")
            return render_template("highscore_sp.html", score = session['correct'], username = session['username'],
            category = session['category'], highscoretext = highscoretext, highscoredata = highscoredata)

    # If number of high scores is less than 10, add high score
    elif len(highscoredata) < 10:
        if not scoreindatabase:
            db.execute("INSERT INTO sp_highscore (uuid, username, score, category) VALUES (:uuid, :username, :score, :category)",
            uuid = session["id"],
            username =  session['username'],
            score = session['correct'],
            category = session['category'])
            highscoredata = db.execute("SELECT * FROM sp_highscore ORDER BY score DESC")
            return render_template("highscore_sp.html", score = session['correct'], username = session['username'],
            category = session['category'], highscoretext = highscoretext, highscoredata = highscoredata)

        else:
            if session['correct'] > scoreindatabase[0]["score"]:
                db.execute("UPDATE sp_highscore SET score = :score, category = :category WHERE username = :username",
                score = session['correct'],
                category = session['category'],
                username = session['username'])
                highscoredata = db.execute("SELECT * FROM sp_highscore ORDER BY score DESC")
                return render_template("highscore_sp.html", score = session['correct'], username = session['username'],
                category = session['category'], highscoretext = highscoretext, highscoredata = highscoredata)

            return render_template("highscore_sp.html", highscoredata = highscoredata, score = session['correct'])

    # If score is higher than lowest high score, add score to high score
    if session['correct'] > highscores[0]["score"]:
        highscoretext = "Congratulations! You made it into the high scores!"

        # Adds user to high score database
        if not scoreindatabase:
            db.execute("INSERT INTO sp_highscore (uuid, username, score, category) VALUES (:uuid, :username, :score, :category)",
            uuid = session["id"],
            username =  session['username'],
            score = session['correct'],
            category = session['category'])


            db.execute("DELETE FROM sp_highscore WHERE score = :score AND username = :username",
            score = highscores[0]["score"],
            username = highscoresnames[0]["username"])


            highscoredata = db.execute("SELECT * FROM sp_highscore ORDER BY score DESC")

            return render_template("highscore_sp.html", score = session['correct'], username = session['username'],
            category = session['category'], highscoretext = highscoretext, highscoredata = highscoredata)

        # Else updates highscore
        else:
            if session['correct'] > scoreindatabase[0]["score"]:
                db.execute("UPDATE sp_highscore SET score = :score, category = :category WHERE username = :username",
                score = session['correct'],
                category = session['category'],
                username = session['username'])
                highscoredata = db.execute("SELECT * FROM sp_highscore ORDER BY score DESC")
                return render_template("highscore_sp.html", score = session['correct'], username = session['username'],
                category = session['category'], highscoretext = highscoretext, highscoredata = highscoredata)

            return render_template("highscore_sp.html", highscoredata = highscoredata, score = session['correct'])

    return render_template("highscore_sp.html", highscoredata = highscoredata, score = session['correct'])

@app.route("/highscore_mp")
def highscore_mp():
    return render_template("highscore_mp.html")


@app.route("/sp_question", methods=["GET", "POST"])
def sp_question():
    from sp_question import get_question


    session['username'] = str(request.args.get("username", ""))
    user_id = str(session["id"])
    category = session['category']
    difficulty = session['difficulty']

    get_question(user_id, session['username'],  category, difficulty)
    return jsonify(True)


# checks and handles answers and time-outs for questions
@app.route("/correct", methods=["GET", "POST"])
def correct():
    # if answer is correct, add score point
    if request.args.get("data", "") == request.args.get("answer", ""):
        session["correct"] += 1

    # delete question from sp_question db
    db.execute("DELETE FROM sp_questions WHERE correct = :correct AND uuid = :session_id", correct = request.args.get("data", ""), session_id = session['id'])
    # db.execute("DELETE FROM sp_questions WHERE correct = :correct", correct = request.args.get("data", ""))
    return jsonify(True)