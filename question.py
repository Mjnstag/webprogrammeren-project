import requests
from random import shuffle
import html

def get_question(category, difficulty):

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

    question_data = requests.get(f"https://opentdb.com/api.php?amount=1&category={category}&difficulty={difficulty}&type=multiple").json()['results'][0]

    # Get question and decodes keys
    question = html.unescape(question_data['question'])
    # Gets correct answer of question and decodes keys
    correct_answer = html.unescape(question_data['correct_answer'])
    # Puts all incorrect answers in a list and decodes them
    incorrect_answers = [html.unescape(i) for i in question_data['incorrect_answers']]
    # Makes list of all possible answers
    all_answers = [correct_answer] + incorrect_answers
    # Randomize answer order
    shuffle(all_answers)

    # remove when done
    # print correct answer for testing purposes
    print(correct_answer)

    # return question data to page
    return question, all_answers, correct_answer



