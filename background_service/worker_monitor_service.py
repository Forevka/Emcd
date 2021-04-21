from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

from aiogram import exceptions
from asyncpg.connection import Connection
from config import TOKEN
from database.models.account_coin_notification_worker import \
    AccountCoinNotificationWorker
from database.user_repo import UserRepository
from enums.lang import Lang
from loguru import logger
from notifier.telegram_notifier import TelegramNotifier
from third_party.emcd_client.client import EmcdClient

from background_service.base_background_service import BaseBackgroundService


@dataclass
class WorkerChangeStatusDataModel:
    old_status: int
    new_status: int
    name: str

    def to_description(self, text: str, localisation: Dict[str, str]) -> str:
        return text.format(
            worker_name=self.name, 
            previous_status=localisation[f'status_{self.old_status}'], 
            new_status=localisation[f'status_{self.new_status}'],
        )

        
class WorkerMonitorService(BaseBackgroundService[AccountCoinNotificationWorker]):
    async def get_notifier(self,):
        return TelegramNotifier(TOKEN)

    async def get_items_to_process(self, con: Connection) -> List[AccountCoinNotificationWorker]:
        user_repo = UserRepository(con)
        return await user_repo.get_all_account_to_refresh()
        
    async def job(self, con: Connection, item: AccountCoinNotificationWorker, notifier: TelegramNotifier, locales: Dict):
        now = datetime.now()

        message_text = ''
        user_repo = UserRepository(con)

        async with EmcdClient(item.account_id) as client:
            api_account = await client.get_workers(item.coin_id)
            if (api_account is None):
                logger.info(f'{item.account_id}|{item.coin_id} - is none')
                return

            user_account = next((acc for acc in await user_repo.get_accounts(item.user_id) if acc.account_id == item.account_id), None)

            logger.info(f'{item.account_id}|{item.coin_id} - Scraped worker info')
            workers = api_account.get_all_workers(item.id)

            await user_repo.update_account_coin(item.id, item.user_id, item.account_id, item.coin_id, item.address, api_account, item.is_active, now)

            logger.info(f'{item.account_id}|{item.coin_id} - Total workers count {len(workers)}')

            if (workers):
                user_db = await user_repo.get_user(item.user_id)

                user_locale = Lang(user_db.lang_id)
                translation = locales[user_locale.name]

                change_status_descr = []
                blacklisted_workers = [w.worker_id for w in await user_repo.get_blacklisted_workers(item.user_id)]

                previous_worker_state = await user_repo.get_previous_worker_state_for_account(item.id)
                for worker in workers:
                    previous_state = next((w for w in previous_worker_state if w.worker_id == worker.worker), None)
                    if (previous_state):
                        if (previous_state.status_id != worker.status_id):
                            logger.info(f'{item.account_id}|{item.coin_id} - worker changed status {worker.worker}')
                            if (worker.worker not in blacklisted_workers):
                                change_status_descr.append(
                                    WorkerChangeStatusDataModel(
                                        previous_state.status_id,
                                        worker.status_id,
                                        previous_state.worker_id
                                    )
                                )
                            else:
                                logger.info(f'{item.account_id}|{item.coin_id} - {worker.worker} blacklisted')
                                if (worker.status_id == -1):
                                    logger.info(f'{item.account_id}|{item.coin_id} - {worker.worker} dead, need to delete from blacklist')
                                    await user_repo.toggle_worker_blacklist(item.user_id, worker.worker)


                logger.info(f'{item.account_id}|{item.coin_id} - Sending notification {item.id}')
                if (change_status_descr):
                    descr = [st.to_description(translation['worker_changed_status_descr'], translation) for st in change_status_descr]
                    message_text = translation['worker_changed_status_body'].format(account_name=user_account.username, description='\n'.join([i for i in descr]))
                    try:
                        await notifier.notify(message_text, con, user_db.id,)
                    except (exceptions.BotBlocked, exceptions.UserDeactivated) as e:
                        logger.warning(f'{item.user_id} blocked bot or deactivated they telegram account, disabling notifications')
                        await user_repo.update_notification_setting(item.user_id, False)
                    except exceptions.TelegramAPIError as e:
                        logger.error(f'aiogram error {e}')

                logger.info(f'{item.account_id}|{item.coin_id} - Clean up worker history {item.id}')
                await user_repo.cleanup_worker_history_for_account(item.id)

                logger.info(f'{item.account_id}|{item.coin_id} - Storing to database')

                await user_repo.store_coin_account_worker_history(workers, now)
                logger.info(f'{item.account_id}|{item.coin_id} - Stored')


