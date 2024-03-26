from openai import OpenAI
from openai.types import Moderation
from openai.types.chat.chat_completion import Choice

from env import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def moderate(input):
    modration_result: list[Moderation] = client.moderations.create(input=input).results
    boolean_result = [int(i.flagged) for i in modration_result]
    return boolean_result


def ask_gpt(system, question, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": question},
                  {"role": "system", "content": system}],
        stream=False,
    )
    choices: list[Choice] = response.choices
    choice: Choice = choices[0]
    return choice.message.content
