import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3 import Retry

import api_aidevs
import api_openai

"""
Authorize and retrieve text of the task
"""
token = api_aidevs.auth("scraper")
task_json: dict = api_aidevs.get_task(token)

"""
Solution goes below
"""

system = task_json['msg']
resource_url = task_json['input']
question = task_json['question']


def fetch_file_as_firefox(url):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0'
    }
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    response = session.get(url, headers=headers)
    return response.text


# Example usage
text = fetch_file_as_firefox(resource_url)
answer = api_openai.ask_gpt(system, question=question)

"""
Sending solution of the task
"""
print("***** Sending answer *****")
response: Response = api_aidevs.send_answer(token, answer, debug=True)