from config import TOKEN, postgres
from bot import on_startup, start_polling
from aiogram import Dispatcher


def start():
    start_polling(TOKEN, postgres)


if __name__ == "__main__":
    start()