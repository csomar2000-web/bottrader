import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class RLAgent(nn.Module):
    def __init__(self, state_dim, action_dim, hidden=256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden),
            nn.ReLU(),
            nn.Linear(hidden, action_dim)
        )
        self.optimizer = optim.Adam(self.parameters(), lr=1e-4)

    def forward(self, x):
        return self.net(x)

    def act(self, state):
        with torch.no_grad():
            q = self.forward(torch.tensor(state, dtype=torch.float32))
        return int(torch.argmax(q).item())

    def train_batch(self, batch, gamma=0.99):
        s, a, r, ns, d = batch
        q = self.forward(s)
        q_val = q.gather(1, a.long())

        nq = self.forward(ns)
        max_next = torch.max(nq, dim=1)[0].unsqueeze(1)
        target = r + gamma * max_next * (1 - d)

        loss = (q_val - target.detach()).pow(2).mean()
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return float(loss.item())
