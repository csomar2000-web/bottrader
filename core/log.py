import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }

        if hasattr(record, "context") and isinstance(record.context, dict):
            log.update(record.context)

        return json.dumps(log)


def setup_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    root.addHandler(handler)


def get_logger(name: str, **context):
    logger = logging.getLogger(name)

    class ContextAdapter(logging.LoggerAdapter):
        def process(self, msg, kwargs):
            ctx = self.extra.copy()
            if "context" in kwargs:
                ctx.update(kwargs["context"])
            kwargs["context"] = ctx
            return msg, kwargs

    return ContextAdapter(logger, context)
