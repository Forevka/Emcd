
from bot import start_polling
from config import TOKEN, CONNECTION_STRING


def start():
    start_polling(TOKEN, CONNECTION_STRING)


if __name__ == "__main__":
    start()
