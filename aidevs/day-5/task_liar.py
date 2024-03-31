import api_aidevs
from api_openai import ask_gpt


def validate_relevation_of_answer(question, answer):
    result = ask_gpt(system=f"""Sprawdzasz czy podana odpowiedź jest zgodna z tematem pytania. Jeżeli jest zgodna odpowiadasz 'YES', jeżeli nie jest zgodna odpowiadasz 'NO'.
    Pytanie brzmi: '{question}'""", question=answer)

    print(f"validation result: {result}")

    return result

QUESTION = "What is capital of Poland?"

token = api_aidevs.auth("liar")
task_json: dict = api_aidevs.get_task(token)

answer = api_aidevs.send_question(token, QUESTION)

validation_result = validate_relevation_of_answer(question=QUESTION, answer=answer)

api_aidevs.send_answer(token, validation_result)
