import logging
import sys
from logging.handlers import RotatingFileHandler
import json
from datetime import datetime, UTC
import os


class StructuredLogger:
    def __init__(self, name, log_file="logs/trading_bot.log"):
        # Ensure log directory exists
        os.makedirs("logs", exist_ok=True)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            # Console output
            console = logging.StreamHandler(sys.stdout)
            console.setFormatter(logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            ))

            # Rotating file handler
            file = RotatingFileHandler(
                log_file, maxBytes=10 * 1024 * 1024, backupCount=5
            )
            file.setFormatter(logging.Formatter(
                "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
            ))

            self.logger.addHandler(console)
            self.logger.addHandler(file)

    # ----------------------------------------------------------------------
    # Core logging functions
    # ----------------------------------------------------------------------
    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg, exc_info=False):
        self.logger.error(msg, exc_info=exc_info)

    def debug(self, msg):
        self.logger.debug(msg)

    # ----------------------------------------------------------------------
    # Structured logging
    # ----------------------------------------------------------------------
    def _utc_timestamp(self):
        """Returns ISO 8601 UTC timestamp (timezone-aware)."""
        return datetime.now(UTC).isoformat()

    def event(self, category, data):
        entry = {
            "timestamp": self._utc_timestamp(),
            "category": category,
            "data": data
        }
        self.logger.info(json.dumps(entry))

    def log_trade(self, trade_data: dict):
        entry = {
            "timestamp": self._utc_timestamp(),
            "type": "trade",
            "data": trade_data
        }
        self.logger.info(json.dumps(entry))

    def log_signal(self, signal_data: dict):
        entry = {
            "timestamp": self._utc_timestamp(),
            "type": "signal",
            "data": signal_data
        }
        self.logger.info(json.dumps(entry))


# Global logger instance
trading_logger = StructuredLogger("TradingBot")
