import os
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import requests
import uuid
import time


# configure flask
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


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

# handles question display
@app.route("/question", methods=["GET", "POST"])
def disp_question():

    # if method is post, render page
    if request.method == 'POST':
        return render_template('question.html')

    else:
        # import function
        from disp_question import question
        # save relevant data
        gamemode = session["gamemode"]
        uuid = session["id"]
        correct_answered = session["correct"]

        # call function and save returns
        data = question(gamemode, uuid, correct_answered)

        # if no remainging question, redirect to highscores
        if data == False:
            return redirect("/highscore")
        # if question, renedr question with relevant data
        return render_template('question.html', progress=data[0],  answered=data[1], question=data[2], answers=data[3], correct_answer=data[4])


# renders categories page or redirects to next page
@app.route("/categories", methods=["GET", "POST"])
def categories():
    if request.method == 'POST':
        # save relevant data
        session['category'] = request.form["Categories"]
        session['difficulty'] = request.form["Difficulty"]

        # redirect to next page
        return redirect('type_game')

    # render page
    return render_template("categories.html")


# renders game type page
@app.route("/type_game")
def type_game():
    return render_template("type_game.html")


# resets correct score, renders singleplayer page, redirect to question
@app.route("/classicgame", methods=["GET", "POST"])
def classicgame():
    if request.method == "POST":
        # save relevant data in session
        session["correct"] = 0
        session["username"] = request.form.get('username')
        session["gamemode"] = "standard"

        time.sleep(2)
        return redirect("/question")
    # save relevant data
    session["correct"] = 0
    session["gamemode"] = "standard"

    return render_template("classicgame.html")


# handles start of custom game
@app.route("/customgame", methods=["GET", "POST"])
def rendercustomgame():
    # if post:
    if request.method == "POST":
        time.sleep(3)
        return redirect("/question")
    # if get
    return render_template("customgame.html")


# handles custom game questions
@app.route("/customgamequestions", methods=["GET", "POST"])
def customgame():
    # import function
    from customgame import get_question

    # save relevant data
    session['username'] = str(request.args.get("username", ""))
    user_id = str(session["id"])
    category = session['category']
    difficulty = session['difficulty']
    session["correct"] = 0
    session["gamemode"] = "custom"
    session["amount"] = str(request.args.get("amount", ""))
    print(session["amount"])
    print(session["username"])

    # put questions in databse
    get_question(user_id, session['username'], category, difficulty, session["amount"])

    # return
    return jsonify(True)


# handles highscore data
@app.route("/highscore")
def highscores():
    # import function
    from highscore import highscore

    # save relevant data
    uuid = session["id"]
    username = session['username']
    score = session['correct']
    category = session['category']

    # set amount of questions
    if session["gamemode"] == "custom":
        amount = session["amount"]
    else:
        # classic game is 10 questions
        amount = 10

    # return highscore data
    return highscore(uuid, username, score, category, amount)


# calls on function to put questions in database
@app.route("/classic_question", methods=["GET", "POST"])
def sp_question():
    # import function from .py file
    from classic_question import get_question

    # get needed variables
    session['username'] = str(request.args.get("username", ""))
    user_id = str(session["id"])
    category = session['category']
    difficulty = session['difficulty']

    # call function to add questions in database
    get_question(user_id, session['username'],  category, difficulty)

    # return
    return jsonify(True)


# handles answer checking and time-outs for questions
@app.route("/correct", methods=["GET", "POST"])
def correct():
    # import function
    from correct import check_correct

    # if answer is correct, update score
    if request.args.get("correct", "") == request.args.get("answer", ""):
        session["correct"] += 1

    # delete question from database
    check_correct(session["gamemode"], request.args.get("correct", ""), session['id'])
    return jsonify(True)