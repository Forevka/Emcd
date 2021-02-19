from aiogram.utils.callback_data import CallbackData

menu_cb = CallbackData('menu', 'type', 'action', 'id')  # menu:<type>:<action>
#menu:account:add:_
#menu:account:open:0
#menu:account:delete:0

coin_account_cb = CallbackData('c_acc', 'action', 'id') # c_acc:<action>:<id>
#c_acc:off:12
#c_acc:on:15