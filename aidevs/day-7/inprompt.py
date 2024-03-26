import concurrent

from tqdm import tqdm

import openai_proxy
import task_api

instruction = "Answer question precisely. No comments.\n"
context = "Context```{}```"

def extract_name(text: str):
    instruction = """Extract name from text. Eg. Ben, Mateusz, Jacob. Eg. 'Ben ma szare oczy' -> Ben
    If you don't know name, deduct it from sense of sentence - find subject of sentence.
    No allowed making up name 
    No special characters allowed in response [,.?]
    No additional comments allowed"""
    name = openai_proxy.ask_gpt(system=instruction, question=text, model="gpt-3.5-turbo")
    return name


token = task_api.auth("inprompt")
task_json: dict = task_api.get_task(token)

input: list = task_json['input']
question: list = task_json['question']

# db: dict = {item.split()[0]: item for item in input}

# Use ThreadPoolExecutor for I/O bound tasks
db: dict = dict()
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(extract_name, input))

    # Do something with the results
    db = dict(zip(results, input))


# # db: dict = {extract_name(item): item for item in input}
related_sentences = "\n".join([value for key, value in db.items() if key in question])

# print("\n\n\n****************")
# print(db)

context = context.format(related_sentences)
system = instruction + context

answer = openai_proxy.ask_gpt(system=system, question=question)

print(f"Answer: {answer}")
task_api.send_answer(token, answer)