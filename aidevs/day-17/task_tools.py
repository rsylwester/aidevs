import json
from typing import Sequence, List

from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.tools import BaseTool, FunctionTool
from llama_index.llms.openai import OpenAI
from openai.types.chat import ChatCompletionMessageToolCall
from requests import Response

import api_aidevs
import apis

"""
Authorize and retrieve text of the task
"""
token = api_aidevs.auth("tools")
task_json: dict = api_aidevs.get_task(token)

"""
Solution goes below
"""

"""
Classify question to one of categories:
"""
question = task_json['question']

add_task_todo_list = FunctionTool.from_defaults(fn=apis.add_task_todo_list)
add_event_to_calendar = FunctionTool.from_defaults(fn=apis.add_event_to_calendar)

llm = OpenAI(temperature=0, model="gpt-4")


class Agent:
    def __init__(self, tools: Sequence[BaseTool] = [], llm: OpenAI = llm):
        self._llm = llm
        self._tools = {tool.metadata.name: tool for tool in tools}

    def ask(self, message: str) -> dict:
        chat_history: List[ChatMessage] = [
            ChatMessage(role="system",
                        content="Skip any comments or questions. Respond with one of predefined in context functions."),
            ChatMessage(role="user", content=message)
        ]
        tools = [tool.metadata.to_openai_tool() for _, tool in self._tools.items()]

        ai_message = self._llm.chat(chat_history, tools=tools).message
        tool_calls = ai_message.additional_kwargs.get("tool_calls", None)

        if tool_calls is not None:
            return self._call_function(tool_calls[0])

        return ai_message.content

    def _call_function(
            self, tool_call: ChatCompletionMessageToolCall
    ) -> dict:
        function_call = tool_call.function
        tool = self._tools[function_call.name]
        return tool(**json.loads(function_call.arguments)).raw_output


agent: Agent = Agent(tools=[add_task_todo_list, add_event_to_calendar], llm=llm)

answer = agent.ask(question)

print(f"{question}: {answer}")

print("***** Sending answer *****")
response: Response = api_aidevs.send_answer(token, answer, debug=True)
