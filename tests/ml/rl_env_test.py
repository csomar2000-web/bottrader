import sys, os
sys.path.insert(0, os.getcwd())

from ml.rl.environment import TradingEnvironment
import numpy as np


def test_env_reset():
    env = TradingEnvironment()
    state = env.reset()

    assert isinstance(state, np.ndarray)
    assert state.shape[0] > 0


def test_env_step():
    env = TradingEnvironment()
    env.reset()

    action = 1  # buy
    next_state, reward, done, info = env.step(action)

    assert isinstance(next_state, np.ndarray)
    assert isinstance(reward, float)
    assert isinstance(done, bool)
    assert isinstance(info, dict)
