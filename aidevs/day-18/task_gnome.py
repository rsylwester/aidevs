from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from requests import Response

import api_aidevs

"""
Authorize and retrieve text of the task
"""
token = api_aidevs.auth("gnome")
task_json: dict = api_aidevs.get_task(token)

"""
Solution goes below
"""

image_url = task_json['url']
msg = task_json['msg']

client = ChatOpenAI(temperature=0.5, model="gpt-4-vision-preview", max_tokens=1024)

answer = client.invoke(
    [HumanMessage(
        content=[
            {"type": "text", "text": "Jakiego koloru jest czapka? Jeśli nie ma czapki zwróć kod błędu 'ERROR'"},
            {"type": "image_url", "image_url": {"url": image_url}},
        ])]
)

print(f"Answer: {answer}")

print("***** Sending answer *****")
response: Response = api_aidevs.send_answer(token, answer.content, debug=True)
