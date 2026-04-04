"""Telegram file sending skill for OpenClaw."""

import os
import time
import logging
from typing import Optional, Dict, Any

try:
    import requests
except ImportError:
    requests = None

logger = logging.getLogger(__name__)

# Configuration keys
ENV_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"
ENV_DEFAULT_CHAT_ID = "TELEGRAM_DEFAULT_CHAT_ID"


def _get_bot_token() -> str:
    """Retrieve bot token from environment or config."""
    token = os.getenv(ENV_BOT_TOKEN)
    if not token:
        raise ValueError(f"Telegram bot token not set. Set {ENV_BOT_TOKEN} environment variable.")
    return token


def _get_default_chat_id() -> Optional[str]:
    """Retrieve default chat ID from environment or config."""
    return os.getenv(ENV_DEFAULT_CHAT_ID)


def send_file(
    file_path: str,
    chat_id: Optional[str] = None,
    bot_token: Optional[str] = None,
    caption: Optional[str] = None,
    max_retries: int = 3,
    backoff_factor: float = 1.5
) -> Dict[str, Any]:
    """
    Send a file to Telegram via bot API.

    Args:
        file_path: Path to file to upload (must exist)
        chat_id: Telegram chat ID. If None, uses TELEGRAM_DEFAULT_CHAT_ID.
        bot_token: Bot token. If None, reads from TELEGRAM_BOT_TOKEN.
        caption: Optional message caption
        max_retries: Number of retry attempts on failure
        backoff_factor: Exponential backoff multiplier

    Returns:
        dict: Telegram API response with 'ok' key. On error, 'ok' is False and 'error' contains message.
    """
    if requests is None:
        return {"ok": False, "error": "requests library not installed"}

    # Resolve chat_id
    if chat_id is None:
        chat_id = _get_default_chat_id()
        if not chat_id:
            return {"ok": False, "error": "No chat_id provided and TELEGRAM_DEFAULT_CHAT_ID not set"}

    # Resolve bot_token
    if bot_token is None:
        try:
            bot_token = _get_bot_token()
        except ValueError as e:
            return {"ok": False, "error": str(e)}

    # Validate file exists
    if not os.path.isfile(file_path):
        return {"ok": False, "error": f"File not found: {file_path}"}

    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

    attempt = 0
    while attempt <= max_retries:
        try:
            with open(file_path, "rb") as f:
                files = {"document": f}
                data = {"chat_id": chat_id}
                if caption:
                    data["caption"] = caption

                logger.info(f"Sending file {file_path} to Telegram chat {chat_id}")
                response = requests.post(url, data=data, files=files, timeout=30)
                response.raise_for_status()
                result = response.json()

                if result.get("ok"):
                    logger.info(f"Telegram send success: message_id={result.get('message_id')}")
                    return result
                else:
                    error_msg = result.get("description", "Unknown Telegram API error")
                    logger.warning(f"Telegram API error: {error_msg}")
                    return {"ok": False, "error": error_msg}

        except requests.exceptions.RequestException as e:
            attempt += 1
            if attempt > max_retries:
                logger.error(f"Telegram send failed after {max_retries} retries: {e}")
                return {"ok": False, "error": f"Network error: {str(e)}"}
            sleep_time = backoff_factor ** (attempt - 1)
            logger.info(f"Retrying Telegram send in {sleep_time:.1f}s (attempt {attempt}/{max_retries})")
            time.sleep(sleep_time)

        except Exception as e:
            logger.exception(f"Unexpected error sending Telegram file: {e}")
            return {"ok": False, "error": f"Unexpected error: {str(e)}"}

    # Should not reach here
    return {"ok": False, "error": "Max retries exceeded"}


# Convenience wrapper using defaults from config
def send_file_with_config(file_path: str, chat_id: Optional[str] = None, caption: Optional[str] = None) -> Dict[str, Any]:
    """
    Send file using configured bot token and default chat ID.
    This is the preferred entry point for agents.
    """
    return send_file(file_path=file_path, chat_id=chat_id, bot_token=None, caption=caption)
