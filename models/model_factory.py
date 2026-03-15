
from .gemini import GeminiWrapper

MAP = {
    "gemini": GeminiWrapper,
}

def get_model(model, model_name):
    model_class = MAP.get(model.lower())
    if not model_class:
        raise ValueError(f"Model '{model_name}' not found in MAP. Available models: {list(MAP.keys())}")
    return model_class(model_name=model_name)