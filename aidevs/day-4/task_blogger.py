import api_openai
import api_aidevs

token = api_aidevs.auth("blogger")
task_json: dict = api_aidevs.get_task(token)

system = """Znassz się na robieniu pizzy i piszesz książkę. Napisz rozdział na z podany tytuł. Rozdział powinien mieć max 100 słów."""

chapters = list()
for chapter_title in task_json['blog']:
    chapters.append(api_openai.ask_gpt(system, chapter_title))

print(chapters)
api_aidevs.send_answer(token, chapters)

