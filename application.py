import os
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import requests
import uuid


# configure flask
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# configure database


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
        from disp_question import question

        gamemode = session["gamemode"]
        uuid = session["id"]
        correct_answered = session["correct"]

        data = question(gamemode, uuid, correct_answered)

        if data == False:
            return redirect("/highscore_sp")

        return render_template('question.html', progress = data[0],  answered = data[1], question = data[2], answers = data[3], correct_answer = data[4])


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
        session["username"] = request.form.get('username')

        # makes sure to redirect to right high score database later
        session["gamemode"] = "standard"
        return redirect("/question")
    session["correct"] = 0
    session["gamemode"] = "standard"

    return render_template("singleplayer.html")


@app.route("/customgame", methods=["GET", "POST"])
def rendercustomgame():


    if request.method == "POST":
        session["correct"] = 0
        session["gamemode"] = "custom"
        session["username"] = request.form.get('username')
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
def highscores():

    from highscore import highscore_sp
    uuid = session["id"]
    username = session['username']
    score = session['correct']
    category = session['category']
    amount = session["amount"]

    return highscore_sp(uuid, username, score, category, amount)

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
    from correct import check_correct
    # if answer is correct, add score point
    if request.args.get("correct", "") == request.args.get("answer", ""):
        session["correct"] += 1

    check_correct(session["gamemode"], request.args.get("correct", ""), session['id'])
    return jsonify(True)
