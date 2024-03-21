from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Now you can access the environment variables using os.getenv
AIDEVS_API_KEY = os.getenv("AIDEVS_API_KEY")
AIDEVS_AUTH_URL = "https://tasks.aidevs.pl/token/{}"
AIDEVS_GET_TASK_URL = "https://tasks.aidevs.pl/task/{}"
AIDEVS_SEND_ANSWER_URL = "https://tasks.aidevs.pl/answer/{}"

