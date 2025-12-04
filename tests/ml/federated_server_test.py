import sys, os
sys.path.insert(0, os.getcwd())

from ml.federated.federated_server import FederatedServer
import numpy as np


def test_federated_aggregation():
    server = FederatedServer()

    grads = [
        np.array([1.0, 2.0, 3.0]),
        np.array([2.0, 2.0, 2.0]),
        np.array([3.0, 2.0, 1.0]),
    ]

    agg = server.aggregate(grads)

    assert np.allclose(agg, np.array([2.0, 2.0, 2.0]))
