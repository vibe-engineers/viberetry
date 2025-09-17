"""Tests for the VibeRetry class."""

from unittest.mock import Mock, patch, call

import pytest

from viberetry.config.config import VibeRetryConfig
from viberetry.models.models import RetryResult
from viberetry.utils.logger import console_logger
from viberetry.viberetry import VibeRetry


@pytest.fixture
def mock_vibe_llm_client():
    """Fixture to mock the VibeLlmClient."""
    with patch("viberetry.viberetry.VibeLlmClient") as mock_client:
        yield mock_client


def test_viberetry_init(mock_vibe_llm_client: Mock):
    """Test the __init__ method of VibeRetry."""
    mock_llm_instance = Mock()
    mock_vibe_llm_client.return_value = mock_llm_instance

    client = Mock()
    model = "test-model"
    config = VibeRetryConfig()

    viberetry_instance = VibeRetry(client, model, config=config)

    mock_vibe_llm_client.assert_called_once_with(
        client, model, config, console_logger
    )
    assert viberetry_instance.llm is mock_llm_instance


def test_decorated_function_success_no_retry(mock_vibe_llm_client: Mock):
    """Test that the decorated function is not retried on success."""
    mock_llm_instance = Mock()
    mock_vibe_llm_client.return_value = mock_llm_instance

    viberetry_instance = VibeRetry(Mock(), "test-model")

    @viberetry_instance
    def successful_function():
        return "Success"

    result = successful_function()

    assert result == "Success"
    mock_llm_instance.vibe_eval.assert_not_called()


@patch("time.sleep")
def test_decorated_function_retry_on_failure(
    mock_sleep: Mock, mock_vibe_llm_client: Mock
):
    """Test that the decorated function is retried on failure."""
    mock_llm_instance = Mock()
    # First call fails, LLM says retry. Second call succeeds.
    mock_llm_instance.vibe_eval.side_effect = [
        RetryResult(should_retry=True, delay=1)
    ]
    mock_vibe_llm_client.return_value = mock_llm_instance

    viberetry_instance = VibeRetry(Mock(), "test-model")

    mock_func = Mock()
    mock_func.side_effect = [Exception("fail"), "Success"]

    @viberetry_instance
    def decorated_function():
        return mock_func()

    result = decorated_function()

    assert result == "Success"
    assert mock_func.call_count == 2
    mock_llm_instance.vibe_eval.assert_called_once()
    mock_sleep.assert_called_once_with(1)


@patch("time.sleep")
def test_decorated_function_no_retry_on_failure(
    mock_sleep: Mock, mock_vibe_llm_client: Mock
):
    """Test that the decorated function is not retried when the LLM says not to."""
    mock_llm_instance = Mock()
    mock_llm_instance.vibe_eval.return_value = RetryResult(
        should_retry=False, delay=0
    )
    mock_vibe_llm_client.return_value = mock_llm_instance

    viberetry_instance = VibeRetry(Mock(), "test-model")

    @viberetry_instance
    def failing_function():
        raise ValueError("fail")

    with pytest.raises(ValueError, match="fail"):
        failing_function()

    mock_llm_instance.vibe_eval.assert_called_once()
    mock_sleep.assert_not_called()


@patch("time.sleep")
def test_max_retries_reached(mock_sleep: Mock, mock_vibe_llm_client: Mock):
    """Test that the decorated function stops retrying after max_retries."""
    mock_llm_instance = Mock()
    # LLM keeps suggesting retries
    mock_llm_instance.vibe_eval.return_value = RetryResult(
        should_retry=True, delay=1
    )
    mock_vibe_llm_client.return_value = mock_llm_instance

    viberetry_instance = VibeRetry(Mock(), "test-model")

    mock_func = Mock(side_effect=Exception("fail"))

    @viberetry_instance(max_retries=2)
    def decorated_function():
        return mock_func()

    with pytest.raises(Exception, match="fail"):
        decorated_function()

    assert mock_func.call_count == 3  # 1 initial call + 2 retries
    assert mock_llm_instance.vibe_eval.call_count == 2
    mock_sleep.assert_has_calls([call(1), call(1)])