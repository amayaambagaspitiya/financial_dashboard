import os
import yaml

def load_config(config_path="conf.yaml") -> dict:
    """
    Load a YAML configuration file and return it as a dictionary.
    """
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    full_path = os.path.join(root_path, config_path)

    with open(full_path, "r") as file:
        config = yaml.safe_load(file)
    return config
