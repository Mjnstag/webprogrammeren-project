import os

from cs50 import SQL
from flask import Flask
from flask import Flask, flash, jsonify, redirect, render_template, request, session

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
db = SQL("sqlite:///sessions.db")


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')