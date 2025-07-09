import json
from pathlib import Path
from .logger import info, warn, error

CONFIG_PATH = Path("config.json")

def load_config():
    """
    Loads configuration from config.json.
    Returns a dictionary with keys like 'last_discord_version' and 'last_bd_version'.
    """
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        except Exception as e:
            error(f"Failed to read config file: {e}")
            return {}
    else:
        return {}

def save_config(discord_version, bd_version):
    """
    Saves the current Discord and BetterDiscord versions into config.json.
    """
    data = {
        "last_discord_version": discord_version,
        "last_bd_version": bd_version
    }

    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump(data, f, indent=2)
        info("Configuration saved to config.json.")
    except Exception as e:
        error(f"Failed to write config file: {e}")