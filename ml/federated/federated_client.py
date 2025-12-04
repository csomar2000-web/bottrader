import numpy as np

class FederatedClient:
    def __init__(self, model, data):
        self.model = model
        self.data = data

    def train(self, epochs=1):
        for _ in range(epochs):
            self.model.step(self.data)
        return self.model.weights()

    def update(self, weights):
        self.model.set_weights(weights)
