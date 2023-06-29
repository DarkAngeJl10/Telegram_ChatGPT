from enum import Enum

import openai
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from settings import BOT_TOKEN, OPENAI_TOKEN, MODEL_NAME, logger, BOT_HISTORY_LENGTH

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
openai.api_key = OPENAI_TOKEN
dp = Dispatcher(bot, storage=storage)
logger.info("Bot has started")


class Role(Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


class MessageHistory:
    def __init__(self):
        self.history = []

    def add_message(self, role: Role, message):
        message = {"role": role.value, "content": message}
        self.history.append(message)

    def clear(self):
        self.history = []
        logger.info("Message History was cleared")

    def get_history(self, history_length=BOT_HISTORY_LENGTH):
        return self.history[-history_length:]


MESSAGE_HISTORY = MessageHistory()


class Form(StatesGroup):
    open_ai_token = State()
    continue_chat = State()
    ready_to_end = State()

@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    logger.info("/start command was invoked")
    await message.answer(
        "Привет, я Телеграм ассистент с помощью ChatGPT\n" "Чтобы начать разговор:\n" "/new_chat"
    )

@dp.message_handler(commands=["new_chat"])
async def new_chat(message: types.Message):
    logger.info("/new_chat command was invoked")
    MESSAGE_HISTORY.clear()
    start_message = "Привет! я твой личный ChatGPT в Telegram :) как я могу помочь тебе?"
    MESSAGE_HISTORY.add_message(Role.SYSTEM, start_message)
    await Form.continue_chat.set()
    await message.answer(start_message)


@dp.message_handler(state=Form.continue_chat)
async def continue_conversation(message: types.Message, state: FSMContext):
    await state.finish()
    user_answer = message.text
    if user_answer == "/new_chat":
        await new_chat(message)
        return

    MESSAGE_HISTORY.add_message(Role.USER, user_answer)
    gpt_response = await get_chatgpt_response(MESSAGE_HISTORY)
    MESSAGE_HISTORY.add_message(Role.ASSISTANT, gpt_response)

    await Form.continue_chat.set()
    await message.answer(gpt_response, parse_mode=types.ParseMode.MARKDOWN)


async def get_chatgpt_response(
    message_history: MessageHistory, history_length=BOT_HISTORY_LENGTH
) -> str:
    logger.info("Query GhatGPT API")
    response = await openai.ChatCompletion.acreate(
        model=MODEL_NAME,
        messages=message_history.get_history(history_length=history_length),
    )
    return response["choices"][0]["message"]["content"]

@dp.message_handler()
async def text(message: types.Message):
    msg = "Привет, я Телеграм ассистент с помощью ChatGPT\n" "Чтобы начать разговор:\n" "/new_chat"
    await message.answer(msg)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)