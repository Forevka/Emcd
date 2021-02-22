from aiogram import Bot

class TelegramNotifier:
    def __init__(self, token: str):
        self.token = token
        self.bot = Bot(token=token, parse_mode='HTML', validate_token=False)

    async def notify(self, user_id: int, text: str):
        await self.bot.send_message(user_id, text,)