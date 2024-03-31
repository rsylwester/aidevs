import api_openai
import api_aidevs

text = "Hawaiian pizza"

token = api_aidevs.auth("embedding")
task_json: dict = api_aidevs.get_task(token)

answer = api_openai.generate_embedding(text)

api_aidevs.send_answer(token, answer)
