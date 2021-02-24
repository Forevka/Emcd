
from bot import start_polling
from config import TOKEN, postgres


def start():
    start_polling(TOKEN, postgres)


if __name__ == "__main__":
    start()
