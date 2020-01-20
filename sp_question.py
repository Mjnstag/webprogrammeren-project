import requests
from random import shuffle
import html
from cs50 import SQL

db = SQL("sqlite:///sessions.db")

def get_question(user_id, username, category, difficulty):
    print(user_id, username, category, difficulty)

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
    for question in question_data:
        question['question'] =  html.unescape(question['question'])
        question['all_answers'] = [html.unescape(i) for i in question["incorrect_answers"]] + [ html.unescape(question['correct_answer'])]

    for number, data in enumerate(question_data, 1):
        db.execute('''INSERT INTO "sp_questions" ("uuid", "username", "question_num", "question","correct", "incorrect1", "incorrect2", "incorrect3") VALUES(?, ?, ?, ?, ?, ?, ?, ?)''',
                        (user_id, username, number,  html.unescape(data['question']),  html.unescape(data['correct_answer']),
                        html.unescape(data['incorrect_answers'][0]),  html.unescape(data['incorrect_answers'][1]),  html.unescape(data['incorrect_answers'][2])))

    # return question data to page
    return question_data



