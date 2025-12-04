import torch
import numpy as np
from ml.rl.agent import RLAgent
from ml.rl.environment import TradingEnvironment

class Trainer:
    def __init__(self, env, agent, batch_size=32):
        self.env = env
        self.agent = agent
        self.batch_size = batch_size
        self.buffer = []

    def push(self, s, a, r, ns, d):
        self.buffer.append((s, a, r, ns, d))
        if len(self.buffer) > 50000:
            self.buffer.pop(0)

    def sample(self):
        idx = np.random.choice(len(self.buffer), self.batch_size)
        batch = [self.buffer[i] for i in idx]

        s = torch.tensor([b[0] for b in batch], dtype=torch.float32)
        a = torch.tensor([[b[1]] for b in batch], dtype=torch.int32)
        r = torch.tensor([[b[2]] for b in batch], dtype=torch.float32)
        ns = torch.tensor([b[3] for b in batch], dtype=torch.float32)
        d = torch.tensor([[b[4]] for b in batch], dtype=torch.float32)
        return s, a, r, ns, d

    def train(self, episodes=50):
        for _ in range(episodes):
            s = self.env.reset()
            done = False

            while not done:
                a = self.agent.act(s)
                ns, r, done, _ = self.env.step(a)
                self.push(s, a, r, ns, done)
                s = ns

                if len(self.buffer) >= self.batch_size:
                    batch = self.sample()
                    self.agent.train_batch(batch)
