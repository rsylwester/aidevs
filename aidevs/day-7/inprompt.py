import openai_proxy
import task_api

instruction = "Answer question precisely. No comments.\n"
context = "Context```{}```"

token = task_api.auth("inprompt")
task_json: dict = task_api.get_task(token)

input: list = task_json['input']
question: list = task_json['question']

db: dict = {item.split()[0]: item for item in input}
related_sentences = "\n".join([value for key, value in db.items() if key in question])

context = context.format(related_sentences)
system = instruction + context

answer = openai_proxy.ask_gpt(system=system, question=question)

task_api.send_answer(token, answer)