
from .tex_reader import TexReader
from .docx_reader import DocxReader

MAP = {
    "latex": TexReader,
    "docx": DocxReader,
}

def get_reader(file_type, **kwargs):
    reader_class = MAP.get(file_type.lower())
    if not reader_class:
        raise ValueError(f"File type '{file_type}' not found in MAP. Available types: {list(MAP.keys())}")
    return reader_class(**kwargs)