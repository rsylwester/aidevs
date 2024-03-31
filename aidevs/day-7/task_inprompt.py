import concurrent

from tqdm import tqdm

import api_openai
import api_aidevs

instruction = "Answer question precisely. No comments.\n"
context = "Context```{}```"

def extract_name(text: str):
    instruction = """Extract name from text. Eg. Ben, Mateusz, Jacob. Eg. 'Ben ma szare oczy' -> Ben
    If you don't know name, deduct it from sense of sentence - find subject of sentence.
    No allowed making up name 
    No special characters allowed in response [,.?]
    No additional comments allowed"""
    name = api_openai.ask_gpt(system=instruction, question=text, model="gpt-3.5-turbo")
    return name


token = api_aidevs.auth("inprompt")
task_json: dict = api_aidevs.get_task(token)

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

answer = api_openai.ask_gpt(system=system, question=question)

print(f"Answer: {answer}")
api_aidevs.send_answer(token, answer)