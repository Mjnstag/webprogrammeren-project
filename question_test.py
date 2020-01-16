import requests
from random import shuffle
import html
from cs50 import SQL
db = SQL("sqlite:///sessions.db")

def get_question(category, difficulty):
    print(requests.get('https://opentdb.com/api_token.php?command=request').json())
    token = "d5b81af019cc27eefe99cdc47a362aae96fbe3fd7075116974a8e05b6617c76"
    print(category, difficulty)

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

    question_data = requests.get(f"https://opentdb.com/api.php?amount=5&category={category}&difficulty={difficulty}&type=multiple").json()['results']
    for question in question_data:
        question['question'] =  html.unescape(question['question'])
        question['all_answers'] = [html.unescape(i) for i in question["incorrect_answers"]] + [ html.unescape(question['correct_answer'])]
    print(question_data)

    # db.execute('''INSERT INTO "sessions" ("questions","answers") VALUES(?, ?)''',
    #                 (question_data, dict()))

    # # Get question and decodes keys
    # question = html.unescape(question_data['question'])
    # # Gets correct answer of question and decodes keys
    # correct_answer = html.unescape(question_data['correct_answer'])
    # # Puts all incorrect answers in a list and decodes them
    # incorrect_answers = [html.unescape(i) for i in question_data['incorrect_answers']]
    # # Makes list of all possible answers
    # all_answers = [correct_answer] + incorrect_answers
    # # Randomize answer order
    # shuffle(all_answers)

    # remove when done
    # print correct answer for testing purposes
    print(question_data)

    # return question data to page
    return question_data



