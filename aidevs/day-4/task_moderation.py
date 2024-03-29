import openai_proxy
import task_api

token = task_api.auth("moderation")
task_json: dict = task_api.get_task(token)

moderation_result = openai_proxy.moderate(task_json['input'])
task_api.send_answer(token, moderation_result)

