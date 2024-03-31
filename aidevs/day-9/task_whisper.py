import os

import requests
from requests import Response

import api_openai
import api_aidevs


def download_mp3(url, filepath):
    response = requests.get(url, stream=True)
    # Check if the request succeeded
    if response.status_code == 200:
        # Set up the local file path

        # Write the content to the local file
        with open(filepath, 'wb') as outfile:
            for chunk in response.iter_content(chunk_size=8192):
                outfile.write(chunk)
        print(f'Successfully saved {filepath}')
    else:
        print(f'Failed to download the file ({response.status_code})')


"""
Authorize and retrieve text of the task
"""
token = api_aidevs.auth("whisper")
task_json: dict = api_aidevs.get_task(token)


"""
Issue solving
"""
url = "https://tasks.aidevs.pl/data/mateusz.mp3"
filepath = os.path.join(os.path.curdir, "mateusz.mp3")

answer = api_openai.transcribe(filepath)

"""
Sending solution of the task
"""
response: Response = api_aidevs.send_answer(token, answer)

"""
Additional logic on CORRECT solution
"""
if response.json()['note'] == 'CORRECT':
    os.remove(filepath)
