import time
import numpy as np
from core.logger import trading_logger


class OrderExecutor:
    def __init__(self, cfg):
        self.cfg = cfg

    def execute(self, order, exchange, market):
        """
        Takes an order, computes execution price/size,
        returns a standardized fill dictionary.
        """
        price = self._fill_price(order, market)
        size = self._fill_size(order, market)

        filled = {
            "type": order.get("type", "open"),           # open / close
            "symbol": order.get("symbol", "BTCUSDT"),    # FIXED
            "side": order["side"],                       # long/short or buy/sell
            "price": price,
            "size": size,
            "timestamp": time.time(),
            "exchange": exchange
        }

        # Structured logging
        trading_logger.log_trade(filled)

        return filled

    def _fill_price(self, order, market):
        """
        Determines executed price with slippage model.
        """
        slip = self.cfg.get("slippage", 0.0)

        side = order["side"].lower()
        if side in ("buy", "long"):
            return market["ask"] * (1 + slip)
        elif side in ("sell", "short"):
            return market["bid"] * (1 - slip)

        # Fallback
        return market["mid"]

    def _fill_size(self, order, market):
        """
        Determines final executed size, respects liquidity & partial fills.
        """
        if not self.cfg.get("partial_fills", True):
            return order["size"]

        max_liquidity = market.get("liq", order["size"])
        return min(order["size"], max_liquidity)
