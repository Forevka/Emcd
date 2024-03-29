from aiogram.utils.callback_data import CallbackData

lang_cb = CallbackData('lang', 'id')

menu_cb = CallbackData('menu', 'type', 'action', 'id')  # menu:<type>:<action>
#menu:account:add:_
#menu:account:open:0
#menu:account:delete:0

conv_cb = CallbackData('conv', 'action', 'id')  # menu:<type>:<action>
flow_cb = CallbackData('flow', 'action', 'id', 'conv_id')

coin_account_cb = CallbackData('c_acc', 'action', 'id') # c_acc:<action>:<id>
#c_acc:off:12
#c_acc:on:15

payouts_cb = CallbackData('payouts', 'id', 'page', 'type')
income_cb = CallbackData('income', 'id', 'page', 'type')
worker_cb = CallbackData('worker', 'id', 'page', 'type', 'status_id')
worker_black_cb = CallbackData('w_bl', 'id', 'page', 'type', 'action')
notification_cb = CallbackData('notif', 'action') #action - on/off
notification_payout_cb = CallbackData('notifp', 'action') #action - on/off
statistic_cb = CallbackData('stat', 'id', 'type')
currency_cb = CallbackData('curr', 'id', 'action')

coins_cb = CallbackData('ch_c', 'id', 'action')

finance_cb = CallbackData('fin', 'id', 'type', 'action', 'page')

delete_account_cb = CallbackData('del_acc', 'id', 'action')

question_answer_cb = CallbackData('faq', 'id', 'page', 'action')

