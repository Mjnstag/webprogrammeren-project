import os

from cs50 import SQL
from flask import Flask
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import requests

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
db = SQL("sqlite:///sessions.db")

@app.route('/', defaults={'path': 'index'})
@app.route('/<path:path>')
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
        question, answers, correct_answer = get_question()

        # send question data to page
        return render_template('question.html', question = question, answers = answers, correct_answer = correct_answer)


@app.route("/categories")
def categories():
    return render_template("categories.html")

