from config import ENVIRONMENT
from aiogram.dispatcher.filters.filters import BoundFilter

class DisableFeatureOnEnvironmentFilter(BoundFilter):
    def __init__(self, env_name: str,):
        self.env_name = env_name

    async def check(self, obj):
        return not (ENVIRONMENT.strip().lower() == self.env_name.strip().lower())