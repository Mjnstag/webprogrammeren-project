import os

from cs50 import SQL
from flask import Flask
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import requests
import uuid

db = SQL("sqlite:///sessions.db")

# define highscore function


def highscore_sp(uuid, username, score, category, amount):

    # checks which game mode has been selected
    if session["gamemode"] == "custom":
        amount = session['amount']

        # collects necessary data from database
        scoreindatabase = db.execute("SELECT score from custom_highscore WHERE username = :username AND amount = :amount",
                                     username=username,
                                     amount=amount)

        highscoredata = db.execute("SELECT * FROM custom_highscore  WHERE amount = :amount ORDER BY score DESC",
                                   amount=amount)
        highscores = db.execute("SELECT score FROM custom_highscore WHERE amount = :amount ORDER BY score ASC",
                                amount=amount)
        highscoresnames = db.execute("SELECT username FROM custom_highscore WHERE amount = :amount ORDER BY score ASC",
                                     amount=amount)
        highscorechanged = 0

        # if highscore database is empty insert user score into table
        if not highscoredata:

            db.execute("INSERT INTO custom_highscore (uuid, username, score, category, amount) VALUES (:uuid, :username, :score, :category, :amount)",
                       uuid=uuid,
                       username=username,
                       score=score,
                       category=category,
                       amount=amount)
            highschorechanged = 1

        # if number of high scores is less than 3, add high score
        elif len(highscoredata) < 3:

            # checks if user does not already have a highscore
            # inserts user highscore
            if not scoreindatabase:
                db.execute("INSERT INTO custom_highscore (uuid, username, score, category, amount) VALUES (:uuid, :username, :score, :category, :amount)",
                           uuid=uuid,
                           username=username,
                           score=score,
                           category=category,
                           amount=amount)
                highscorechanged = 1

            # checks if user has more answers than existing user highscore
            elif session['correct'] > scoreindatabase[0]["score"]:

                # updates user highscore
                db.execute("UPDATE custom_highscore SET score = :score, category = :category, amount = :amount WHERE username = :username",
                           score=score,
                           category=category,
                           username=username,
                           amount=amount)
                highscorechanged = 1

        # checks if user has more correct answers than lowest score in database
        elif session['correct'] > highscores[0]["score"]:

            # checks if user does not already have a highscore
            # adds user to highscore database
            if not scoreindatabase:
                db.execute("INSERT INTO custom_highscore (uuid, username, score, category, amount) VALUES (:uuid, :username, :score, :category, :amount)",
                           uuid=uuid,
                           username=username,
                           score=score,
                           category=category,
                           amount=amount)

                # deletes lowest highscore
                db.execute("DELETE FROM custom_highscore WHERE score = :score AND username = :username AND amount = :amount",
                           score=highscores[0]["score"],
                           username=highscoresnames[0]["username"],
                           amount=amount)

                highscorechanged = 1

            # checks if user beat own highscore
            elif session['correct'] > scoreindatabase[0]["score"]:

                # updates existing user highscore
                db.execute("UPDATE custom_highscore SET score = :score, category = :category, amount = :amount WHERE username = :username",
                           score=score,
                           category=category,
                           username=username,
                           amount=amount)
                highscorechanged = 1
        for place, player in enumerate(highscoredata, 1):
                player['placement'] = place
        if highscorechanged == 1:

            # recollect highscore data
            highscoredata = db.execute("SELECT * FROM custom_highscore WHERE amount = :amount ORDER BY score DESC",
                                       amount=amount)

            # return user and database information to template
            return render_template("highscore_sp.html", score=score, username=username,
                                   category=category, amount=amount, highscoretext=1,
                                   highscoredata=highscoredata, gamemode=1)

        return render_template("highscore_sp.html", amount=amount, highscoredata=highscoredata, score=score, gamemode=1)

    # if user selects classic game mode
    # collects necessary data from database

    scoreindatabase = db.execute("SELECT score from sp_highscore WHERE username = :username AND category = :category",
                                 username=username,
                                 category=category)

    highscoredata = db.execute("SELECT * FROM sp_highscore WHERE category = :category ORDER BY score DESC",
                               category=category)

    highscores = db.execute("SELECT score FROM sp_highscore WHERE category = :category ORDER BY score ASC",
                            category=category)
    highscoresnames = db.execute("SELECT username FROM sp_highscore WHERE category = :category ORDER BY score ASC",
                                 category=category)

    highscorechanged = 0

    # checks if highscore list is empty
    if not highscoredata:

        # inserts user score into highscore database
        db.execute("INSERT INTO sp_highscore (uuid, username, score, category) VALUES (:uuid, :username, :score, :category)",
                   uuid=uuid,
                   username=username,
                   score=score,
                   category=category)
        highscorechanged = 1

    # checks if number of highscores is less than 10
    elif len(highscoredata) < 10:

        # checks if user does not already have a highscore
        # adds highscore to database
        if not scoreindatabase:
            db.execute("INSERT INTO sp_highscore (uuid, username, score, category) VALUES (:uuid, :username, :score, :category)",
                       uuid=uuid,
                       username=username,
                       score=score,
                       category=category)
            highscorechanged = 1

        # checks if new user score beats existing high score
        elif session['correct'] > scoreindatabase[0]["score"]:

            # updates user highscore
            db.execute("UPDATE sp_highscore SET score = :score, category = :category WHERE username = :username",
                       score=score,
                       category=category,
                       username=username)
            highscorechanged = 1

    # checks if user score beats lowest highscore
    elif session['correct'] > highscores[0]["score"]:

        # checks if user is already in highscores
        # adds user to high score database
        if not scoreindatabase:

            # adds user to highscores and deletes lowest highscore
            db.execute("INSERT INTO sp_highscore (uuid, username, score, category) VALUES (:uuid, :username, :score, :category)",
                       uuid=uuid,
                       username=username,
                       score=score,
                       category=category)

            db.execute("DELETE FROM sp_highscore WHERE score = :score AND username = :username",
                       score=highscores[0]["score"],
                       username=highscoresnames[0]["username"])
            highscorechanged = 1

        # checks if user beat his existing highscore
        elif session['correct'] > scoreindatabase[0]["score"]:

            # updates user highscore
            db.execute("UPDATE sp_highscore SET score = :score, category = :category WHERE username = :username",
                       score=score,
                       category=category,
                       username=username)
            highscorechanged = 1

    for place, player in enumerate(highscoredata, 1):
        player['placement'] = place

    if highscorechanged == 1:

        # recollects data
        highscoredata = db.execute("SELECT * FROM sp_highscore WHERE category = :category ORDER BY score DESC",
                                   category=category)

        return render_template("highscore_sp.html", score=score, username=username,
                               category=category, highscoretext=1,
                               highscoredata=highscoredata, gamemode=0)

    return render_template("highscore_sp.html", highscoredata=highscoredata, score=score, gamemode=0)