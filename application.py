import os

from cs50 import SQL
from flask import Flask
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import requests

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQL("sqlite:///sessions.db")

@app.route('/', defaults={'path': 'index'})
# @app.route('/<path:path>')
def catch_all(path):
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
        return render_template('question.html', question = question, answers = answers, correct_answer = correct_answer)


@app.route("/categories", methods=["GET", "POST"])
def categories():
    print(requests.get("https://opentdb.com/api_category.php").json()['trivia_categories'])
    if request.method == 'POST':
        session['category'] = request.form["Categories"]
        session['difficulty'] = request.form["Difficulty"]
        print(session['category'])
        print(session['difficulty'])
        return redirect('question')
    return render_template("categories.html")

