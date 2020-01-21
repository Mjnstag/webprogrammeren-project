import os

from cs50 import SQL
from flask import Flask
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import requests
import uuid

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQL("sqlite:///sessions.db")

@app.route('/', defaults={'path': 'homepage'})
# @app.route('/<path:path>')
def catch_all(path):
    session["id"] = str(uuid.uuid4())
    return render_template(path + '.html')


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
        print(answers)
        correct_answer = db.execute("SELECT correct FROM sp_questions WHERE uuid = :uuid",
        uuid = session["id"])
        correct_answer = correct_answer[0]["correct"]
        print(correct_answer)
        #print(db.execute("SELECT correct, incorrect1, incorrect2, incorrect3, question_num FROM sp_questions WHERE uuid = :uuid ORDER BY question_num DESC", uuid = session["id"]))
        #db.execute("DELETE FROM sp_questions WHERE question_num = 1")
        return render_template('question.html', question = question, answers = answers, correct_answer = correct_answer)


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


@app.route("/question_test")
def test():

    if request.method == 'POST':
        # render page
        return render_template('question_test.html')
    else:
        # import question.py
        from question_test import get_question

        # get question data
        question_data = get_question("general", "easy")
        return render_template("question_test.html", list = [i for i in range(10)], data = question_data)


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
    session["correct answers"] = 0
    return render_template("singleplayer.html")


@app.route("/joinmp", methods=["GET", "POST"])
def joinmp():
    if request.method == "POST":
        return redirect("/question")
    return render_template("joinmp.html")

@app.route("/createmp", methods=["GET", "POST"])
def createmp():
    if request.method == "POST":
        return redirect("/question")
    return render_template("createmp.html")

@app.route("/highscore_sp")
def highscore_sp():
    print(session["correct"])
    # insert user data
    # select top for highscores
    # send top to page
    return render_template("highscore_sp.html", score = session['correct'], username = session['username'], category = session['category'])


@app.route("/highscore_mp")
def highscore_mp():
    return render_template("highscore_mp.html")


@app.route("/test")
def test_page():
    from question_test import get_question
    return render_template("test.html", data = get_question("general", "easy"))


@app.route("/sp_question", methods=["GET", "POST"])
def sp_question():
    from sp_question import get_question


    session['username'] = str(request.args.get("username", ""))
    user_id = str(session["id"])
    category = session['category']
    difficulty = session['difficulty']

    get_question(user_id, session['username'],  category, difficulty)
    return jsonify(True)


@app.route("/correct", methods=["GET", "POST"])
def correct():
    print("test")
    print(str(request.args.get("data", "")))
    if request.args.get("data", "") == request.args.get("answer", ""):
        session["correct"] += 1
    db.execute("DELETE FROM sp_questions WHERE correct = :correct",
    correct = str(request.args.get("data", "")))
    return jsonify(True)


# met ajax een request sturen als een antwoord goed is en dan een session var aanpassen?
# @app.route("/correct_answer", methods=["GET"])
# def correct_answer():
#     print('test')
#     session["correct answers"] += 1
#     return jsonify(succes = True, correct = session["correct answers"])