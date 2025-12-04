from ml.rl.agent import RLAgent
from ml.rl.environment import TradingEnvironment

class RLModeSwitch:
    def __init__(self, cfg, market):
        self.cfg = cfg
        self.market = market
        self.agent = None
        self.env = None
        self.enabled = False

    def activate(self):
        self.enabled = True
        self.env = TradingEnvironment(self.market, self.cfg)
        self.agent = RLAgent(self.cfg["state_dim"], self.cfg["action_dim"])

    def deactivate(self):
        self.enabled = False

    def act(self, state):
        if not self.enabled:
            return None
        return self.agent.act(state)
