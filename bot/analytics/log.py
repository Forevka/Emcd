import logging
from datetime import datetime
import aiohttp

from aioinflux import InfluxDBClient, InfluxDBWriteError
from config import ENVIRONMENT, INFLUX_WRITE_TIMEOUT_SEC, InfluxDBParams

async def log_callback_query(user_id: int, event: str):
    data = {
        "measurement": "bot_callback",
        "time": datetime.now(),
        "fields": {"event": 1},
        "tags": {
            "user": str(user_id),
            "callback_query": event
        }
    }
    return await log(data)

async def log_text(user_id: int, event: str):
    data = {
        "measurement": "bot_text",
        "time": datetime.now(),
        "fields": {"event": 1},
        "tags": {
            "user": str(user_id),
            "text_code": event
        }
    }
    return await log(data)

async def log_command(user_id: int, event: str):
    data = {
        "measurement": "bot_commands",
        "time": datetime.now(),
        "fields": {"event": 1},
        "tags": {
            "user": str(user_id),
            "command": event
        }
    }
    return await log(data)
    
async def log_request(update_id: int):
    data = {
        "measurement": "bot_requests",
        "time": datetime.now(),
        "fields": {"event": 1},
        "tags": {
            "update_id": update_id,
        }
    }
    return await log(data)


async def log(data: dict):
    try:
        async with InfluxDBClient(host=InfluxDBParams.STATS_HOST, db=InfluxDBParams.STATS_DB,
                                username=InfluxDBParams.STATS_USER, password=InfluxDBParams.STATS_PASS, timeout=INFLUX_WRITE_TIMEOUT_SEC) as client:
            await client.write(data)
    except InfluxDBWriteError as ex:
        logging.error(f"InfluxDB write error: {str(ex)}")