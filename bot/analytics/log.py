import logging
from datetime import datetime

from aioinflux import InfluxDBClient, InfluxDBWriteError
from config import InfluxDBParams

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
    try:
        async with InfluxDBClient(host=InfluxDBParams.STATS_HOST, db=InfluxDBParams.STATS_DB,
                                  username=InfluxDBParams.STATS_USER, password=InfluxDBParams.STATS_PASS) as client:
            await client.write(data)
    except InfluxDBWriteError as ex:
        logging.error(f"InfluxDB write error: {str(ex)}")
