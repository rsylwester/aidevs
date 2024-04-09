import json
from typing import Sequence, List

from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.tools import BaseTool, FunctionTool
from openai.types.chat import ChatCompletionMessageToolCall
from requests import Response

import api_aidevs
import apis
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI

"""
Authorize and retrieve text of the task
"""
token = api_aidevs.auth("knowledge")
task_json: dict = api_aidevs.get_task(token)

"""
Solution goes below
"""

"""
Classify question to one of categories:
"""
question = task_json['question']

get_current_exchange_rate_tool = FunctionTool.from_defaults(fn=apis.get_current_exchange_rate)
get_current_population_tool = FunctionTool.from_defaults(fn=apis.get_current_population)
answer_general_question_tool = FunctionTool.from_defaults(fn=apis.answer_general_question)

llm = OpenAI(temperature=0, model="gpt-3.5-turbo")


class Agent:
    def __init__(self, tools: Sequence[BaseTool] = [], llm: OpenAI = llm):
        self._llm = llm
        self._tools = {tool.metadata.name: tool for tool in tools}

    def ask(self, message: str) -> str:
        chat_history: List[ChatMessage] = [ChatMessage(role="system", content=instruction)]

        chat_history.append(ChatMessage(role="user", content=message))
        tools = [
            tool.metadata.to_openai_tool() for _, tool in self._tools.items()
        ]

        ai_message = self._llm.chat(chat_history, tools=tools).message
        additional_kwargs = ai_message.additional_kwargs
        chat_history.append(ai_message)

        tool_calls = additional_kwargs.get("tool_calls", None)
        if tool_calls is not None:
            for tool_call in tool_calls:
                function_message = self._call_function(tool_call)
                return function_message.content

        return ai_message.content

    def _call_function(
            self, tool_call: ChatCompletionMessageToolCall
    ) -> ChatMessage:
        id_ = tool_call.id
        function_call = tool_call.function
        tool = self._tools[function_call.name]
        output = tool(**json.loads(function_call.arguments))
        return ChatMessage(
            name=function_call.name,
            content=str(output),
            role="tool",
            additional_kwargs={
                "tool_call_id": id_,
                "name": function_call.name,
            },
        )


agent: Agent = Agent(
    tools=[get_current_exchange_rate_tool, get_current_population_tool, answer_general_question_tool], llm=llm)

answer = agent.ask(question)

print("***** Sending answer *****")
response: Response = api_aidevs.send_answer(token, answer, debug=True)
