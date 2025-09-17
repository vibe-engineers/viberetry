from dotenv import load_dotenv

load_dotenv()

import os

from google import genai

from viberetry import VibeRetry

# create a google gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# create a vibegen instance using the above client and specify a model
# model variants for gemini: https://ai.google.dev/gemini-api/docs/models#model-variations
viberetry = VibeRetry(client, model="gemini-2.0-flash-lite")

# the example below simulates a function that always raises an exception
# to demonstrate the retry mechanism
@viberetry(max_retries=3, remarks="use exponential backoff")
def simulate_failure() -> int:
    """
    This function raises a simulated exception to demonstrate the retry mechanism.
    """
    raise Exception("Simulated exception.")


print(simulate_failure())