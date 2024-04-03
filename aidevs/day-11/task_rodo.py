from requests import Response

import api_aidevs

"""
Authorize and retrieve text of the task
"""
token = api_aidevs.auth("rodo")
task_json: dict = api_aidevs.get_task(token)

"""
Solution goes below
"""

system = """
Use placeholders in place real data related to your personality.

Strict rules you’re obligated to follow throughout the conversation:
- always skip any additional comments.
- replace your name with %imie%
- replace your surname with %nazwisko%
- replace your occupation with %zawod%
- replace place of living with %miasto%
- use original language
- Communicate truthfully as possible" 
"""


"""
Sending solution of the task
"""
print("***** Sending answer *****")
response: Response = api_aidevs.send_answer(token, system, debug=True)
