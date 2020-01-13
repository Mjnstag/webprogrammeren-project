import os

from cs50 import SQL
from flask import Flask
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import requests

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
db = SQL("sqlite:///sessions.db")


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template(index)

@app.route("/question", methods=["GET", "POST"])
def disp_question():
    from question import question
    questions = question()
    return render_template('question.html', test = questions)