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


url = "https://tasks.aidevs.pl/data/mateusz.mp3"
filepath = os.path.join(os.path.curdir, "mateusz.mp3")

token = api_aidevs.auth("whisper")
task_json: dict = api_aidevs.get_task(token)

answer = api_openai.transcribe(filepath)

response: Response = api_aidevs.send_answer(token, answer)

if response.json()['note'] == 'CORRECT':
    os.remove(filepath)