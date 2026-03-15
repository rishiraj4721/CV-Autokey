
import re
from .base_reader import BaseReader

class TexReader(BaseReader):
    """
    This reader is designed to handle .tex files, specifically those that follow common resume formats. 
    It looks for sections labeled "Experience" and "Skills" using both the resume.cls format and a more generic LaTeX section format.
    Example resume is available in input/resume.tex for testing.
    """
    def __init__(self):
        super().__init__()

    def extract_experience(self, file_path):
        """Reads a .tex file and extracts the content of the 'Experience' section."""
        content = self.read(file_path)

        # Try matching \begin{rSection}{EXPERIENCE}...\end{rSection} first (for resume.cls)
        match = re.search(r'\\begin\{rSection\}\{EXPERIENCE\}(.*?)\\end\{rSection\}', content, re.DOTALL | re.IGNORECASE)
        
        # Fall back to \section{Experience} pattern if not found
        if not match:
            match = re.search(r'\\section\s*\{\s*Experience\s*\}(.*?)(?=\\section|\\subsection|\\begin\{rSection\}|\\end\{document\}|$)', content, re.DOTALL | re.IGNORECASE)
        
        if match:
            return match.group(1).strip()
        return ""

    def extract_skills(self, file_path):
        """Reads a .tex file and extracts the content of the 'Skills' section."""
        content = self.read(file_path)

        # Try matching \begin{rSection}{SKILLS}...\end{rSection} first (for resume.cls)
        match = re.search(r'\\begin\{rSection\}\{SKILLS\}(.*?)\\end\{rSection\}', content, re.DOTALL | re.IGNORECASE)
        
        # Fall back to \section{Skills} pattern if not found
        if not match:
            match = re.search(r'\\section\s*\{\s*Skills\s*\}(.*?)(?=\\section|\\subsection|\\begin\{rSection\}|\\end\{document\}|$)', content, re.DOTALL | re.IGNORECASE)
        
        if match:
            return match.group(1).strip()
        return ""
