import logging
import os

BOT_HISTORY_LENGTH = os.getenv("BOT_HISTORY_LENGTH", 6)

logger = logging.getLogger("gpt_chat")
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

BOT_TOKEN = os.getenv("BOT_TOKEN", "Your Api key")
if not BOT_TOKEN:
    logging.error(
        "BOT_TOKEN env var is not found, cannot start the bot without it, create it with @BotFather Telegram bot! "
    )
else:
    logging.info("BOT_TOKEN found, starting the bot")

OPENAI_TOKEN = os.getenv("OPENAI_TOKEN", "Your Api key")
if not OPENAI_TOKEN:
    logging.error(
        "OPENAI_TOKEN env var is not found, cannot start the ChatGPT without it, create on OpenAI API Keys "
    )
else:
    logging.info("OPENAI_TOKEN found, starting the ChatGPT")

DEFAULT_MODEL_NAME = "gpt-3.5-turbo"
MODEL_NAME = os.getenv("MODEL_NAME")
if not MODEL_NAME:
    MODEL_NAME = DEFAULT_MODEL_NAME
    logging.info(f"MODEL_NAME env var is not found, using default model {MODEL_NAME}")
else:
    logging.info(f"MODEL_NAME is {MODEL_NAME}")