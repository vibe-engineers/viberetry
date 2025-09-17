"""Configuration objects for VibeRetry."""

from typing import Any

from vibetools._internal import VibeConfig


class VibeRetryConfig(VibeConfig):
    """
    Configuration for VibeRetry, extending the base VibeConfig.

    This configuration sets a default system instruction for the LLM.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the VibeRetryConfig object.

        Args:
            *args: Positional arguments to pass to the parent VibeConfig.
            **kwargs: Keyword arguments to pass to the parent VibeConfig.
                      'system_instruction' is given a default value.

        """
        kwargs.setdefault(
            "system_instruction",
            (
                "You are a function. Return ONLY a valid JSON STRING, with no code fences, "
                "no markdown formatting, and no explanations. It must have EXACTLY two keys:\n"
                '  "should_retry": a boolean (true or false)\n'
                '  "delay": an integer number of seconds\n'
                "Do not include any text before or after the JSON. Output must look like:\n"
                '{"should_retry": false, "delay": 0}'
            ),
        )

        super().__init__(*args, **kwargs)
