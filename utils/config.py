import yaml
from typing import Dict, Any


class YAMLConfig:
    """A simple class to read YAML configuration files."""
    
    def __init__(self, config_file: str):
        """
        Initialize YAMLConfig with a config file path.
        
        Args:
            config_file: Path to the YAML configuration file
        """
        self.config_file = config_file
    
    def read(self) -> Dict[str, Any]:
        """
        Read and return the YAML configuration as a dictionary.
        
        Returns:
            Dictionary containing the YAML configuration
            
        Example:
            config = YAMLConfig("config.yaml")
            data = config.read()
        """
        config = {}
        with open(self.config_file, "r") as f:
            config = yaml.safe_load(f)
        if config is None or not self.validate(config):
            raise ValueError(f"Invalid configuration in {self.config_file}. Required keys are missing.")
        return config

    def validate(self, config: Dict[str, Any]) -> bool:
        """
        Validate that all required keys are present in the configuration.
        
        Args:
            config: The configuration dictionary to validate
            
        Returns:
            True if all required keys are present, False otherwise
            
        Example:
            config = YAMLConfig("config.yaml")
            if config.validate(["database", "api_key", "debug"]):
                print("Config is valid")
            else:
                print("Missing required keys")
        """
        required_keys = [
            "role",
            "model",
            "input_format",
            "input",
            "output_format",
            "output"
        ]
        for key in required_keys:
            if key not in config:
                return False
        return True
