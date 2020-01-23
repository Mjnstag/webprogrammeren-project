import requests
from random import shuffle
import html
from cs50 import SQL

db = SQL("sqlite:///sessions.db")

def get_question(room_id, category, difficulty):

    # Get question data from api
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

    question_data = requests.get(f"https://opentdb.com/api.php?amount=10&category={category}&difficulty={difficulty}&type=multiple").json()['results']

    for number, data in enumerate(question_data, 1):
        db.execute('''INSERT INTO "mp_question" ("room_id", "question_num", "question", "correct", "incorrect1", "incorrect2", "incorrect3") VALUES(?, ?, ?, ?, ?, ?, ?)''',
                        (room_id, number,  html.unescape(data['question']),  html.unescape(data['correct_answer']).replace("'", ''),
                        html.unescape(data['incorrect_answers'][0]).replace("'", ''),  html.unescape(data['incorrect_answers'][1]).replace("'", ''),  html.unescape(data['incorrect_answers'][2]).replace("'", '')))

    # return question data to page
    return question_data



