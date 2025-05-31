import yaml

def load_config(config_path: str = "config/config.yaml") -> dict: #here it is going to take from config folder ----->config.yaml and return dict
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config