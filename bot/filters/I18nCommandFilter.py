from aiogram.dispatcher.filters.filters import BoundFilter

class I18nCommandFilter(BoundFilter):
    def __init__(self, command_code: str,):
        self.command_code = command_code

    async def check(self, obj):
        from bot.common.lang import reversed_locales
        obj.command_code = 'unknown'
        
        c_user_locale_code = obj.c_user_locale_code
        
        t = obj.text.lower()
        if (t in reversed_locales[c_user_locale_code]):
            is_filtered = reversed_locales[c_user_locale_code][t] == self.command_code
            if (is_filtered):
                obj.command_code = self.command_code
            return is_filtered

        return False