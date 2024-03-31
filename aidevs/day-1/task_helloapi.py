import api_aidevs

token = api_aidevs.auth("helloapi")
task_json: dict = api_aidevs.get_task(token)

api_aidevs.send_answer(token, task_json['cookie'])

