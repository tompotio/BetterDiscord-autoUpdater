import sys
from .discord_utils import (
    get_discord_version,
    is_discord_running,
    kill_discord,
    launch_discord
)
from .betterdiscord_utils import (
    get_latest_release,
    download_installer,
    run_installer
)
from .config_utils import load_config, save_config
from .logger import info, warn, error

def perform_update(force=False):
    """
    Main update flow:
    - Detects current versions.
    - Downloads and installs BetterDiscord if needed.
    - Restarts Discord if it was running.
    """
    # Step 1: Get current Discord version
    info("Checking installed Discord version...")
    discord_version = get_discord_version()
    if not discord_version:
        error("Could not detect Discord version. Aborting.")
        sys.exit(1)
    info(f"Detected Discord version: {discord_version}")

    # Step 2: Get latest BetterDiscord release
    info("Checking latest BetterDiscord release...")
    bd_version, bd_url, bd_name = get_latest_release()
    if not bd_version or not bd_url:
        error("Failed to fetch BetterDiscord release info.")
        sys.exit(1)
    info(f"Latest BetterDiscord version: {bd_version}")

    # Step 3: Load config and compare
    config = load_config()
    last_discord = config.get("last_discord_version")
    last_bd = config.get("last_bd_version")

    if not force and discord_version == last_discord and bd_version == last_bd:
        info("No updates detected. Installation skipped.")
        return

    if force:
        warn("Force mode enabled. Proceeding with installation.")

    # Step 4: Download installer
    installer_path = download_installer(bd_url, bd_name)
    if not installer_path:
        error("Failed to download installer. Aborting.")
        sys.exit(1)

    # Step 5: Check if Discord is running
    was_running = is_discord_running()
    if was_running:
        info("Discord is currently running. Attempting to close it.")
        kill_discord()

    # Step 6: Install BetterDiscord
    run_installer(installer_path)

    # Step 7: Restart Discord if needed
    if was_running:
        launch_discord()

    # Step 8: Save updated config
    save_config(discord_version, bd_version)