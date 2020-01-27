import requests
import html
from cs50 import SQL

db = SQL("sqlite:///sessions.db")

def get_question(user_id, username, category, difficulty, num_of_questions):

    # format variables
    if category == 'art':
        category = '25'
    elif category == 'general':
        category = '9'
    elif category == 'geography':
        category = '22'
    elif category == 'history':
        category = '23'
    elif category == 'sports':
        category = '21'
    elif category == 'science_nature':
        category = '17'

    # get questions based on difficulty and category
    question_data = requests.get(f"https://opentdb.com/api.php?amount={num_of_questions}&category={category}&difficulty={difficulty}&type=multiple").json()['results']

    # add questiondata into database
    for number, data in enumerate(question_data, 1):
        db.execute('''INSERT INTO "customgame" ("uuid", "username", "question_num", "question","correct", "incorrect1", "incorrect2", "incorrect3") VALUES(?, ?, ?, ?, ?, ?, ?, ?)''',
                        (user_id, username, number,  html.unescape(data['question']),  html.unescape(data['correct_answer']).replace("'", ''),
                        html.unescape(data['incorrect_answers'][0]).replace("'", ''),  html.unescape(data['incorrect_answers'][1]).replace("'", ''),  html.unescape(data['incorrect_answers'][2]).replace("'", '')))

    # return to application.py
    return None
