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
        return render_template('question.html')
    else:
        from question import get_question

        question, answers, correct_answer = get_question()

        return render_template('question.html', question = question, answers = answers, correct_answer = correct_answer)

@app.route("/options")
def options():
    return render_template("options.html")