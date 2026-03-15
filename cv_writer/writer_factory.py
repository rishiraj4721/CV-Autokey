
from .tex_writer import TexWriter

MAP = {
    "latex": TexWriter,
}

def get_writer(format_name):
    writer_class = MAP.get(format_name.lower())
    if not writer_class:
        raise ValueError(f"Writer for format '{format_name}' not found in MAP. Available formats: {list(MAP.keys())}")
    return writer_class()