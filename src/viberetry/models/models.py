"""Models for the VibeRetry library."""

from typing import TypedDict


class RetryResult(TypedDict):
    """Result of a retry evaluation."""

    should_retry: bool
    delay: int
