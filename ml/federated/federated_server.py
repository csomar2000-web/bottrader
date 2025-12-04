# import numpy as np

# class FederatedServer:
#     """
#     Minimal Federated Server implementation matching test suite.
#     """

#     def __init__(self, model=None, clients=None):
#         self.model = model
#         self.clients = clients or []

#     def aggregate(self):
#         """
#         Test expects simple mean aggregation of client updates.
#         """
#         if not self.clients:
#             return 0

#         updates = [c.get_update() for c in self.clients]
#         return float(np.mean(updates))
import numpy as np

class FederatedServer:

    def __init__(self, model=None, clients=None):
        self.model = model
        self.clients = clients or []

    def aggregate(self, gradients):
        # TEST EXPECTS: simple mean of numpy arrays
        grads = [np.asarray(g, dtype=float) for g in gradients]
        return np.mean(grads, axis=0)
