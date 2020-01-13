import requests

def question():
    temp = requests.get("https://opentdb.com/api.php?amount=2&type=multiple")
    print(requests.get('https://opentdb.com/api_category.php'))
    print(temp.json()['results'])
    return temp.json()