from dataclasses import dataclass

@dataclass
class WorkerBlacklist:
    user_id: int
    worker_id: str

    __select__ = """ select "user_id", "worker_id" from worker_blacklist"""