
from typing import override
from docx import Document

from .base_reader import BaseReader


class DocxReader(BaseReader):
    def __init__(self):
        super().__init__()

    @override
    def read(self, file_path):
        document = Document(file_path)
        full_text = []
        for para in document.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)

    def extract_experience(self, file_path):
        pass

    def extract_skills(self, file_path):
        pass
