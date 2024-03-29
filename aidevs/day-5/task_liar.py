import openai_proxy
import task_api
from validator import validate_relevation_of_answer

QUESTION = "What is capital of Poland?"

token = task_api.auth("liar")
task_json: dict = task_api.get_task(token)

answer = task_api.send_question(token, QUESTION)

validation_result = validate_relevation_of_answer(question=QUESTION, answer=answer)

task_api.send_answer(token, validation_result)