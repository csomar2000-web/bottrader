from execution.order_validator import OrderValidator
from execution.order_router import OrderRouter
from execution.order_executor import OrderExecutor

class TradeManager:
    def __init__(self, exchanges, cfg):
        self.validator = OrderValidator(cfg["validator"])
        self.router = OrderRouter(exchanges, cfg["router"])
        self.executor = OrderExecutor(cfg["executor"])
        self.cfg = cfg

    def process(self, order, market):
        if not self.validator.validate(order, market):
            order = self.validator.sanitize(order, market)

        ex_name, ex_conn = self.router.route(order, market)
        fill = self.executor.execute(order, ex_name, market)
        return fill
