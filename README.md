<p align="center">
  <img width=300 src="https://raw.githubusercontent.com/vibe-engineers/viberetry/main/assets/viberetry.png" />
  <h1 align="center">VibeRetry</h1>
</p>

<p align="center">
  <a href="https://github.com/vibe-engineers/viberetry/actions/workflows/ci-cd-pipeline.yml"> <img src="https://github.com/vibe-engineers/viberetry/actions/workflows/ci-cd-pipeline.yml/badge.svg" /> </a>
  <a href="https://pypi.org/project/viberetry/"><img src="https://img.shields.io/pypi/v/viberetry.svg" /></a>
  <a href="https://pypi.org/project/viberetry/"><img src="https://img.shields.io/pypi/pyversions/viberetry.svg" /></a>
  <a href="https://github.com/vibe-engineers/viberetry/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/viberetry.svg" /></a>
  <a href="https://pepy.tech/project/viberetry"><img src="https://pepy.tech/badge/viberetry" /></a>
</p>

## Table of Contents
* [Introduction](#introduction)
* [Features](#features)
* [Technologies](#technologies)
* [Team](#team)
* [Contributing](#contributing)
* [Others](#others)

### Introduction
**VibeRetry** is a lightweight python package that allows users to use natural language (LLMs) to intelligently retry failed function calls. For example, **VibeRetry** can be used as a decorator to wrap a function and, in the event of an exception, the LLM will decide whether to retry the function and for how long to wait before retrying. It supports OpenAI and Google Gemini clients currently and a simple example illustrating how it can be used can be seen below:
```python
from google import genai
from viberetry import VibeRetry

# create a google gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# create a viberetry instance using the above client and specify a model
viberetry = VibeRetry(client, model="gemini-2.0-flash-lite")

# the example below simulates a function that always raises an exception
# to demonstrate the retry mechanism
@viberetry(max_retries=3, remarks="use exponential backoff")
def simulate_failure() -> int:
    """
    This function raises a simulated exception to demonstrate the retry mechanism.
    """
    raise Exception("Simulated exception.")

# this will fail, but the LLM will retry it a few times
# before finally raising the exception
simulate_failure()
```

**VibeRetry** is published on [**pypi**](https://pypi.org/project/viberetry/) and can be easily installed with:
```bash
python3 -m pip install viberetry
```
Details on the usage of the package and available APIs can be found on the [**wiki page**](https://github.com/vibe-engineers/viberetry/wiki).

### Features
- **Natural Language Conditions**: Use natural language to check for conditions, making your code more readable and intuitive.
- **Multi-provider Support**: Seamlessly switch between different LLM providers. VibeRetry currently supports OpenAI and Google Gemini.
- **Extensible**: The modular design allows for easy extension to other LLM providers in the future.
- **Custom Exceptions**: Provides custom exceptions for better error handling and debugging.

### Technologies
Technologies used by VibeRetry are as below:
##### Done with:

<p align="center">
  <img height="150" width="150" src="https://logos-download.com/wp-content/uploads/2016/10/Python_logo_icon.png"/>
</p>
<p align="center">
Python
</p>

##### Project Repository
```
https://github.com/vibe-engineers/viberetry
```

### Team
* [Kong Le-Yi](https://github.com/konglyyy)
* [Tan Jin](https://github.com/tjtanjin)

### Contributing
If you are looking to contribute to the project, you may find the [**Developer Guide**](https://github.com/vibe-engineers/viberetry/blob/main/docs/DeveloperGuide.md) useful.

In general, the forking workflow is encouraged and you may open a pull request with clear descriptions on the changes and what they are intended to do (enhancement, bug fixes etc). Alternatively, you may simply raise bugs or suggestions by opening an [**issue**](https://github.com/vibe-engineers/viberetry/issues) or raising it up on [**discord**](https://discord.gg/dBW35GBCPZ).

Note: Templates have been created for pull requests and issues to guide you in the process.

### Others
For any questions regarding the implementation of the project, you may also reach out on [**discord**](https://discord.gg/dBW35GBCPZ).

