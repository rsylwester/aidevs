import requests
from requests import Response

from aidevs import env


def auth(task):
    data = {
        "apikey": env.AIDEVS_API_KEY
    }

    auth_url = env.AIDEVS_AUTH_URL.format(task)
    print(auth_url)
    response = requests.post(auth_url, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        print()
        print(f"authorized successfully, task: {task}")
        token = response.json()['token']
        return token
    else:
        print("Failed to retrieve auth token", response.status_code)


def send_question(token, question):
    data = {
        "question": question
    }

    print(f"sending question to: {env.AIDEVS_GET_TASK_URL}")
    get_question_url = env.AIDEVS_GET_TASK_URL.format(token)
    response = requests.post(get_question_url, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        print()
        print(f"got answer from aidevs model: {response.json()}")
        answer = response.json()['answer']
        return answer
    else:
        print("Failed to retrieve answer", response.status_code)


def get_task(token, debug=True) -> dict:
    get_question_url = env.AIDEVS_GET_TASK_URL.format(token)
    response = requests.get(get_question_url)

    if debug:
        print("******* task content ******")
        print(response.raw)
        print(response.json())
        print("****************************")

    return response.json()


def send_answer(token, answer, debug=True) -> Response:
    send_answer_url = env.AIDEVS_SEND_ANSWER_URL.format(token)

    answer_body = {"answer": answer}

    response = requests.post(send_answer_url, json=answer_body)

    if debug:
        print(response.json())

    return response
