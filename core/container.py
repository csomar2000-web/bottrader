class Container:
    def __init__(self):
        self.registry = {}

    def register(self, key, provider):
        self.registry[key] = provider

    def resolve(self, key, *args, **kwargs):
        if key not in self.registry:
            raise KeyError(f"Service not found: {key}")
        return self.registry[key](*args, **kwargs)

container = Container()
