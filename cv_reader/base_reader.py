

class BaseReader:
    def __init__(self):
        pass

    def read(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()
    
    def extract_experience(self, file_path):
        """Extract experience information from the given file path. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement this method")
    
    def extract_skills(self, file_path):
        """Extract skills information from the given file path. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement this method")
