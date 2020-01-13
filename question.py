import requests
from random import shuffle
import html

def get_question():
    temp = requests.get("https://opentdb.com/api.php?amount=2&type=multiple").json()['results'][0]
    print(requests.get('https://opentdb.com/api_category.php'))

    question = html.unescape(temp['question'])
    correct_answer = temp['correct_answer']
    incorrect_answers = temp['incorrect_answers']
    all_answers = [correct_answer] + incorrect_answers
    shuffle(all_answers)

    print(correct_answer)

    return question, all_answers, correct_answer