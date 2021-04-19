from aiogram.dispatcher.filters.filters import BoundFilter

class RethrowExceptionFilter(BoundFilter):
    key = 'rethrow'
    required = True
    default = True

    def __init__(self, rethrow: bool,):
        self.rethrow = rethrow

    async def check(self, obj, error):
        if (hasattr(error, 'aiogram_is_handled')):
            return False

        setattr(error, 'aiogram_is_handled', True)

        return True
