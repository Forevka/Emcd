from aiogram.dispatcher.filters.state import State, StatesGroup

# States
class Form(StatesGroup):
    waiting_for_account_id = State()  # Will be represented in storage as 'Form:waiting_for_account_id'