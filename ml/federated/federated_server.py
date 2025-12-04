import numpy as np

class FederatedServer:
    def __init__(self, model, clients):
        self.model = model
        self.clients = clients

    def aggregate(self, client_weights):
        w = [np.array(c) for c in client_weights]
        avg = np.mean(w, axis=0)
        self.model.set_weights(avg.tolist())
        return avg

    def round(self):
        local = []
        for c in self.clients:
            w = c.train()
            local.append(w)
        g = self.aggregate(local)
        for c in self.clients:
            c.update(g)
        return g
