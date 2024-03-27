import openai
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


def generate_embedding(text, engine="text-embedding-ada-002"):
    """
    Generate an embedding for the given text using OpenAI's API.

    Parameters:
    - text (str): The text to generate an embedding for.
    - engine (str): The embedding model to use. Default is "text-embedding-ada-002".

    Returns:
    - A list of floats representing the embedding of the input text.
    """
    # Replace 'your_api_key_here' with your actual OpenAI API key

    response = client.embeddings.create(
        model=engine,
        input=text
    )

    # Extract and return the embedding vector
    embedding_vector = response.data[0].embedding
    return embedding_vector
