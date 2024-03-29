import task_api

token = task_api.auth("helloapi")
task_json: dict = task_api.get_task(token)

task_api.send_answer(token, task_json['cookie'])

