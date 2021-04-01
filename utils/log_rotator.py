import time
import logging.handlers as handlers
from typing import Any, IO

import json


class SizedTimedRotatingFileHandler(handlers.TimedRotatingFileHandler):
    """
    Handler for logging to a set of files, which switches from one file
    to the next when the current file reaches a certain size, or at certain
    timed intervals
    """
    stream: IO[Any]

    def __init__(self, filename, maxBytes=0, backupCount=0, encoding=None,
                    delay=0, when='h', interval=1, utc=False, serialize=False,):
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc)
        self.maxBytes = maxBytes
        self.serialize = serialize

    
    def format(self, record):
        if (self.serialize):
            exception = {}

            if hasattr(record, 'exception'):
                exception.update({
                    "type": None if record.exception.type is None else record.exception.type.__name__,
                    "value": record.exception.value,
                    "traceback": bool(record.exception.traceback),
                })

            serializable = {
                "text": record.msg,
                "record": {
                    "exception": exception,
                    "extra": record.extra,
                    "file": {
                        "name": record.filename, 
                        "path": record.pathname,
                    },
                    "function": record.funcName,
                    "level": {
                        "name": record.levelname,
                        "no": record.levelno,
                    },
                    "line": record.lineno,
                    "message": record.msg,
                    "module": record.module,
                    "name": record.name,
                    "process": {
                        "id": record.process, 
                        "name": record.processName
                    },
                    "thread": {
                        "id": record.thread, 
                        "name": record.threadName
                    },
                    "time": {
                        "timestamp": record.created,
                    },
                },
            }

            return json.dumps(serializable, default=str)

        return super().format(record)

    def shouldRollover(self, record):
        """
        Determine if rollover should occur.

        Basically, see if the supplied record would cause the file to exceed
        the size limit we have.
        """
        if self.stream is None:
            self.stream = self._open()
        if self.maxBytes > 0:
            msg = "%s\n" % self.format(record)
            # due to non-posix-compliant Windows feature
            self.stream.seek(0, 2)
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1
        t = int(time.time())
        if t >= self.rolloverAt:
            return 1
        return 0

