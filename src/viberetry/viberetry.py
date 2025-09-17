"""The main VibeRetry class and its functionalities."""

import json
import time
import traceback
from functools import wraps
from typing import Any, Callable

from vibetools._internal import VibeLlmClient

from viberetry.config.config import VibeRetryConfig
from viberetry.models.models import RetryResult
from viberetry.utils.logger import console_logger


class VibeRetry:
    """
    A class that uses LLMs to perform "vibe retry" on function calls.

    This class is used as a decorator to evaluate whether a function call
    should be retried.
    """

    def __init__(
        self,
        client: VibeLlmClient,
        model: str,
        *,
        config: VibeRetryConfig | dict | None = None,
    ) -> None:
        """
        Initialize the VibeRetry object.

        Args:
            client: An instance of VibeLlmClient.
            model: The name of the model to use for the LLM.
            config: VibeRetryConfig containing runtime knobs (e.g., num_tries).

        """
        if config is None:
            config = VibeRetryConfig()
        elif isinstance(config, dict):
            config = VibeRetryConfig(**config)

        self.llm = VibeLlmClient(client, model, config, console_logger)

    def __call__(
        self, arg: Callable[..., Any] | None = None, *, max_retries: int = 1, remarks: str = ""
    ) -> Callable[..., Any]:
        """
        Decorate a function to catch exceptions and consult the LLM
        for whether to retry and how long to wait.

        Args:
            arg: The function to decorate.
            max_retries: maximum number of retry attempts after a failure (default 1).
            remarks: additional remarks to provide context to the LLM.

        Returns:
            The decorated function.

        """

        def _decorator(func: Callable[..., Any]):
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any):
                # number of retries already performed
                attempts = 0
                # keep (attempt_number, delay_seconds) for prior retries
                historical_attempts: list[dict[str, int]] = []
                while True:
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        if attempts >= max_retries:
                            raise

                        # build concise failure context for the LLM
                        context = {
                            "function_name": func.__name__,
                            "args": repr(args),
                            "kwargs": repr(kwargs),
                            "exception_type": type(e).__name__,
                            "exception_message": str(e),
                            "traceback": "".join(traceback.format_exc()[-4000:]),
                        }

                        prompt = (
                            f"HISTORICAL_ATTEMPTS: {json.dumps(historical_attempts, ensure_ascii=False)}\n"
                            f"ADDITIONAL REMARKS: {remarks}\n"
                            "TASK: Given the following failure context, decide whether to retry and for how long.\n\n"
                            f"CONTEXT:\n{json.dumps(context, ensure_ascii=False)}"
                        )

                        result: RetryResult = self.llm.vibe_eval(prompt, RetryResult)

                        # handle results
                        should_retry = (
                            result.get("should_retry")
                            if isinstance(result, dict)
                            else getattr(result, "should_retry", False)
                        )
                        delay = result.get("delay") if isinstance(result, dict) else getattr(result, "delay", 0)
                        delay = int(delay or 0)

                        if should_retry:
                            # record this upcoming retry (#attempt is 1-based)
                            historical_attempts.append({"attempt": attempts + 1, "delay": delay})
                            if delay > 0:
                                time.sleep(delay)
                            attempts += 1
                            continue

                        # if llm decides not to retry
                        raise

            return wrapper

        # support both @vibe_retry and @vibe_retry(max_retries=...)
        if callable(arg):
            return _decorator(arg)
        return _decorator
