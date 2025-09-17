from dotenv import load_dotenv

load_dotenv()

import os

from openai import Client

from viberetry import VibeRetry

# create an openai client
client = Client(api_key=os.getenv("OPENAI_API_KEY"))

# create a viberetry instance using the above client and specify a model
# model variants for openai: https://platform.openai.com/docs/models
viberetry = VibeRetry(client, model="gpt-4.1-nano")

# the example below simulates a function that always raises an exception
# to demonstrate the retry mechanism
@viberetry(max_retries=3, remarks="use exponential backoff")
def simulate_failure() -> int:
    """
    This function raises a simulated exception to demonstrate the retry mechanism.
    """
    raise Exception("Simulated exception.")


print(simulate_failure())