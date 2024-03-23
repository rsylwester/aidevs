import openai_proxy
import task_api

token = task_api.auth("blogger")
task_json: dict = task_api.get_task(token)

system = """Znassz się na robieniu pizzy i piszesz książkę. Napisz rozdział na z podany tytuł. Rozdział powinien mieć max 100 słów."""

chapters = list()
for chapter_title in task_json['blog']:
    chapters.append(openai_proxy.ask_gpt(system, chapter_title))

print(chapters)
task_api.send_answer(token, chapters)

