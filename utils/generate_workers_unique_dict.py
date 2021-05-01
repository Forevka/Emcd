
from typing import List
from third_party.emcd_client.models.coin_workers import CoinWorker

def generate_unique_workers_dict(workers: List[CoinWorker]):
    return {
        worker.hash_name(): worker.worker for worker in workers
    }