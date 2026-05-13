from typing import Any, Dict
import os
import sys
import yaml


def get_config_path() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


def check_config(config: Dict):
    if config == None:
        raise Exception("config.yaml cannot load.")
    if not config["api_hash"] or not config["api_id"]:
        raise Exception("config api value don't exist.")
    if not config["bot_token"]:
        raise Exception("config bot token value don't exist.")


def load_config() -> Dict[str, Any]:
    current_path = get_config_path()
    config_path = os.path.join(current_path, "config.yaml")
    if not os.path.exists(config_path):
        raise Exception("config.yaml file don't exist.")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        check_config(config)
        return config
