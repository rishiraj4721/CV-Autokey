

class ModelWrapper:
    def __init__(self):
        pass

    def get_client(self):
        raise NotImplementedError("Subclasses must implement this method")

    def generate(self, prompt, **kwargs):
        raise NotImplementedError("Subclasses must implement this method")
