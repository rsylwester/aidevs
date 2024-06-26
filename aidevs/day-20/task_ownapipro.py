import threading
from time import sleep

from flask import Flask, request
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from pyngrok import ngrok

import api_aidevs
from tools import SaveMemoryTool, AnswerTool

token = api_aidevs.auth("ownapipro")
task_json: dict = api_aidevs.get_task(token)

tools = [SaveMemoryTool, AnswerTool]
llm = ChatOpenAI(model="gpt-4")


def invoke_tool(tools, user_message: str):
    llm_with_tools: Runnable[LanguageModelInput, BaseMessage] = llm.bind_tools(tools)

    # input_obj = LanguageModelInput(user_message=user_message)
    input_obj = [
        HumanMessage(content=user_message),
        AIMessage(
            content="I'm calling proper tool.")
    ]

    ai_msg = llm_with_tools.invoke(input_obj)

    for tool_call in ai_msg.tool_calls:
        selected_tool = {AnswerTool.name(): AnswerTool, SaveMemoryTool.name(): SaveMemoryTool}[tool_call["name"]]

        tool_output = selected_tool.invoke(tool_call["args"])
        return tool_output


# system = "always skip any additional comments. dont’t modify content"
# invoke_tool(tools=tools, user_message="Mam na imię Janek")
# result = invoke_tool(tools=tools, user_message="Jak mam na imię?")

"""
Authorize and retrieve text of the task
"""
token = api_aidevs.auth("ownapipro")
task_json: dict = api_aidevs.get_task(token)

openai_client = ChatOpenAI(model="gpt-4")
app = Flask(__name__)


def ask_gpt(question):
    answer = openai_client.invoke(
        [HumanMessage(
            content=[
                {"type": "text", "text": question},
            ])]
    )

    return answer.content


@app.route('/', methods=['POST'])
def api():
    question = request.json['question']
    answer = invoke_tool(tools=tools, user_message=question)

    print(f"{question}: {answer}")

    response = {
        "reply": answer,
    }

    return response


def start_ngrok():
    connection = ngrok.connect(addr="127.0.0.1:5000")
    public_url = connection.public_url
    print(" * ngrok URL: " + public_url + " *")
    return public_url


def send_api_url_with_delay(delay, public_url):
    def send_api_url(public_url: str):
        api_aidevs.send_answer(token, public_url, debug=True)

    sleep(delay)  # Delay execution for a specified number of seconds
    send_api_url(public_url)  # Call the function with the provided arguments


if __name__ == '__main__':
    public_api_url = start_ngrok()

    timer = threading.Thread(target=send_api_url_with_delay, args=(4, public_api_url))  # Set a delay of 5 seconds
    timer.start()

    app.run()
