from strategies.auto.templates.momentum import MomentumStrategy
from strategies.auto.templates.mean_reversion import MeanReversionStrategy

STRATEGY_TEMPLATES = {
    "momentum": MomentumStrategy,
    "mean_reversion": MeanReversionStrategy
}
