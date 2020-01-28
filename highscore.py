import os

from cs50 import SQL
from flask import Flask
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import requests
import uuid

db = SQL("sqlite:///sessions.db")


def highscore_sp(uuid, username, score, category, amount):

    # checks if user is already in database, and only updates when the new score is higher than the existing score

    if session["gamemode"] == "custom":
        amount = session['amount']

        scoreindatabase = db.execute("SELECT score from custom_highscore WHERE username = :username AND amount = :amount",
                                     username=username,
                                     amount=amount)

        highscoredata = db.execute("SELECT * FROM custom_highscore  WHERE amount = :amount ORDER BY score DESC",
                                   amount=amount)
        highscoretext = "Congratulations! You made it into the High Scores!"
        highscores = db.execute("SELECT score FROM custom_highscore WHERE amount = :amount ORDER BY score ASC",
                                amount=amount)
        highscoresnames = db.execute("SELECT username FROM custom_highscore WHERE amount = :amount ORDER BY score ASC",
                                     amount=amount)

        if not highscoredata:

            db.execute("INSERT INTO custom_highscore (uuid, username, score, category, amount) VALUES (:uuid, :username, :score, :category, :amount)",
                       uuid=uuid,
                       username=username,
                       score=score,
                       category=category,
                       amount=amount)
            highscoredata = db.execute("SELECT * FROM custom_highscore WHERE amount = :amount ORDER BY score DESC",
                                       amount=amount)
            for place, player in enumerate(highscoredata, 1):
                player['placement'] = place

            return render_template("highscore_sp.html", score=score, username=username,
                                   category=category, amount=amount, highscoretext=highscoretext,
                                   highscoredata=highscoredata, gamemode=1)

            # if number of high scores is less than 3, add high score
        elif len(highscoredata) < 3:
            if not scoreindatabase:
                db.execute("INSERT INTO custom_highscore (uuid, username, score, category, amount) VALUES (:uuid, :username, :score, :category, :amount)",
                           uuid=uuid,
                           username=username,
                           score=score,
                           category=category,
                           amount=amount)
                highscoredata = db.execute("SELECT * FROM custom_highscore WHERE amount = :amount ORDER BY score DESC",
                                           amount=amount)
                for place, player in enumerate(highscoredata, 1):
                    player['placement'] = place

                return render_template("highscore_sp.html", score=score, username=username,
                                       category=category, amount=amount, highscoretext=highscoretext,
                                       highscoredata=highscoredata, gamemode=1)

            elif session['correct'] > scoreindatabase[0]["score"]:

                db.execute("UPDATE custom_highscore SET score = :score, category = :category, amount = :amount WHERE username = :username",
                           score=score,
                           category=category,
                           username=username,
                           amount=amount)

                highscoredata = db.execute("SELECT * FROM sp_highscore WHERE amount = :amount ORDER BY score DESC",
                                           category=category)
                for place, player in enumerate(highscoredata, 1):
                    player['placement'] = place
                return render_template("highscore_sp.html", score=score, username=username,
                                       category=category, amount=amount, highscoretext=highscoretext,
                                       highscoredata=highscoredata, gamemode=1)

            for place, player in enumerate(highscoredata, 1):
                player['placement'] = place
            return render_template("highscore_sp.html", highscoredata=highscoredata, score=score, amount=amount, gamemode=1)
        elif session['correct'] > highscores[0]["score"]:

            # adds user to high score database
            if not scoreindatabase:
                db.execute("INSERT INTO custom_highscore (uuid, username, score, category, amount) VALUES (:uuid, :username, :score, :category, :amount)",
                           uuid=uuid,
                           username=username,
                           score=score,
                           category=category,
                           amount=amount)

                db.execute("DELETE FROM custom_highscore WHERE score = :score AND username = :username AND amount = :amount",
                           score=highscores[0]["score"],
                           username=highscoresnames[0]["username"],
                           amount=amount)

                highscoredata = db.execute("SELECT * FROM custom_highscore WHERE amount = :amount ORDER BY score DESC",
                                           amount=amount)

                for place, player in enumerate(highscoredata, 1):
                    player['placement'] = place

                return render_template("highscore_sp.html", score=score, username=username,
                                       category=category, amount=amount, highscoretext=highscoretext,
                                       highscoredata=highscoredata, gamemode=1)

                # else updates highscore
            elif session['correct'] > scoreindatabase[0]["score"]:

                db.execute("UPDATE custom_highscore SET score = :score, category = :category WHERE username = :username",
                           score=score,
                           category=category,
                           username=username,
                           amount=amount)
                highscoredata = db.execute("SELECT * FROM sp_highscore WHERE amount = :amount ORDER BY score DESC",
                                           category=category)

                for place, player in enumerate(highscoredata, 1):
                    player['placement'] = place

                return render_template("highscore_sp.html", score=score, username=username,
                                       category=category, amount=amount, highscoretext=highscoretext, highscoredata=highscoredata, gamemode=1)

            for place, player in enumerate(highscoredata, 1):
                player['placement'] = place
            return render_template("highscore_sp.html", amount=amount, highscoredata=highscoredata, score=score, gamemode=1)

        for place, player in enumerate(highscoredata, 1):
            player['placement'] = place
        return render_template("highscore_sp.html", amount=amount, highscoredata=highscoredata, score=score, gamemode=1)

    scoreindatabase = db.execute("SELECT score from sp_highscore WHERE username = :username AND category = :category",
                                 username=username,
                                 category=category)

    highscoredata = db.execute("SELECT * FROM sp_highscore WHERE category = :category ORDER BY score DESC",
                               category=category)

    highscoretext = "Congratulations! You made it into the High Scores!"
    highscores = db.execute("SELECT score FROM sp_highscore WHERE category = :category ORDER BY score ASC",
                            category=category)
    highscoresnames = db.execute("SELECT username FROM sp_highscore WHERE category = :category ORDER BY score ASC",
                                 category=category)

    # checks if highscore list is empty
    if not highscoredata:

        db.execute("INSERT INTO sp_highscore (uuid, username, score, category) VALUES (:uuid, :username, :score, :category)",
                   uuid=uuid,
                   username=username,
                   score=score,
                   category=category)
        highscoredata = db.execute("SELECT * FROM sp_highscore WHERE category = :category ORDER BY score DESC",
                                   category=category)

        for place, player in enumerate(highscoredata, 1):
            player['placement'] = place

        return render_template("highscore_sp.html", score=score, username=username,
                               category=category, highscoretext=highscoretext,
                               highscoredata=highscoredata, gamemode=0)

    # if number of high scores is less than 10, add high score
    elif len(highscoredata) < 10:
        if not scoreindatabase:
            db.execute("INSERT INTO sp_highscore (uuid, username, score, category) VALUES (:uuid, :username, :score, :category)",
                       uuid=uuid,
                       username=username,
                       score=score,
                       category=category)
            highscoredata = db.execute("SELECT * FROM sp_highscore WHERE category = :category ORDER BY score DESC",
                                       category=category)

            for place, player in enumerate(highscoredata, 1):
                player['placement'] = place

            return render_template("highscore_sp.html", score=score, username=username,
                                   category=category, highscoretext=highscoretext,
                                   highscoredata=highscoredata, gamemode=0)

        elif session['correct'] > scoreindatabase[0]["score"]:

            db.execute("UPDATE sp_highscore SET score = :score, category = :category WHERE username = :username",
                       score=score,
                       category=category,
                       username=username)

            highscoredata = db.execute("SELECT * FROM sp_highscore WHERE category = :category ORDER BY score DESC",
                                       category=category)
            for place, player in enumerate(highscoredata, 1):
                player['placement'] = place

            return render_template("highscore_sp.html", score=score, username=username,
                                   category=category, highscoretext=highscoretext,
                                   highscoredata=highscoredata, gamemode=0)

        for place, player in enumerate(highscoredata, 1):
            player['placement'] = place
        return render_template("highscore_sp.html", highscoredata=highscoredata, score=score, gamemode=0)

    elif session['correct'] > highscores[0]["score"]:

        # adds user to high score database

        if not scoreindatabase:
            db.execute("INSERT INTO sp_highscore (uuid, username, score, category) VALUES (:uuid, :username, :score, :category)",
                       uuid=uuid,
                       username=username,
                       score=score,
                       category=category)

            db.execute("DELETE FROM sp_highscore WHERE score = :score AND username = :username",
                       score=highscores[0]["score"],
                       username=highscoresnames[0]["username"])

            highscoredata = db.execute("SELECT * FROM sp_highscore WHERE category = :category ORDER BY score DESC",
                                       category=category)

            for place, player in enumerate(highscoredata, 1):
                player['placement'] = place

            return render_template("highscore_sp.html", score=score, username=username,
                                   category=category, highscoretext=highscoretext, highscoredata=highscoredata, gamemode=0)

        # else updates highscore
        elif session['correct'] > scoreindatabase[0]["score"]:

            db.execute("UPDATE sp_highscore SET score = :score, category = :category WHERE username = :username",
                       score=score,
                       category=category,
                       username=username)
            highscoredata = db.execute("SELECT * FROM sp_highscore WHERE category = :category ORDER BY score DESC",
                                       category=category)

            for place, player in enumerate(highscoredata, 1):
                player['placement'] = place

            return render_template("highscore_sp.html", score=score, username=username,
                                   category=category, highscoretext=highscoretext, highscoredata=highscoredata, gamemode=0)

        for place, player in enumerate(highscoredata, 1):
            player['placement'] = place

        return render_template("highscore_sp.html", highscoredata=highscoredata, score=score, gamemode=0)

    for place, player in enumerate(highscoredata, 1):
        player['placement'] = place
    return render_template("highscore_sp.html", highscoredata=highscoredata, score=score, gamemode=0)
