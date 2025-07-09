import os
import psutil
import subprocess
from pathlib import Path
from .logger import info, warn, error

DISCORD_PATH = Path(os.getenv("LOCALAPPDATA")) / "Discord"

def get_discord_version():
    """
    Returns the currently installed version of Discord as a string.
    Example: "1.0.9199"
    """
    if not DISCORD_PATH.exists():
        warn("Discord is not installed in the expected location.")
        return None

    versions = [f.name for f in DISCORD_PATH.iterdir() if f.name.startswith("app-")]
    if not versions:
        warn("No Discord version folders found.")
        return None

    latest = sorted(versions)[-1]
    return latest.replace("app-", "")

def is_discord_running():
    """
    Returns True if a Discord process is currently running.
    """
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and 'discord' in proc.info['name'].lower():
            return True
    return False

def kill_discord():
    """
    Kills all running Discord processes.
    """
    found = False
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and 'discord' in proc.info['name'].lower():
            found = True
            try:
                proc.kill()
                info(f"Discord process killed (PID {proc.pid})")
            except psutil.NoSuchProcess:
                warn(f"Discord process (PID {proc.pid}) already terminated.")
            except Exception as e:
                error(f"Failed to kill Discord process (PID {proc.pid}): {e}")
    if not found:
        info("No Discord processes detected.")

def launch_discord():
    """
    Launches Discord using Update.exe.
    """
    discord_launcher = DISCORD_PATH / "Update.exe"
    if discord_launcher.exists():
        try:
            subprocess.Popen([str(discord_launcher), "--processStart", "Discord.exe"], shell=False)
            info("Discord has been restarted.")
        except Exception as e:
            error(f"Failed to launch Discord: {e}")
    else:
        warn("Discord launcher not found (Update.exe).")