import api_openai
import api_aidevs

token = api_aidevs.auth("moderation")
task_json: dict = api_aidevs.get_task(token)

moderation_result = api_openai.moderate(task_json['input'])
api_aidevs.send_answer(token, moderation_result)

