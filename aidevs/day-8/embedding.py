import openai_proxy
import task_api

text="Hawaiian pizza"

token = task_api.auth("embedding")
task_json: dict = task_api.get_task(token)

answer = openai_proxy.generate_embedding(text)

task_api.send_answer(token, answer)