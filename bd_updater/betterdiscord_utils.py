import re
import requests
import shutil
import sys
from pathlib import Path
from .logger import info, warn, error

CACHE_DIR = Path("cache")
BETTERDISCORD_REPO = "https://api.github.com/repos/BetterDiscord/Installer/releases/latest"
SETUP_FILENAME_PATTERN = re.compile(r"BetterDiscord-Windows-[\d.]+.exe")

def get_latest_release():
    """
    Returns the latest BetterDiscord version, download URL, and filename.
    """
    headers = {
        "User-Agent": "BetterDiscord-Updater",
        "Accept": "application/vnd.github+json"
    }

    try:
        response = requests.get(BETTERDISCORD_REPO, headers=headers)
        response.raise_for_status()
        data = response.json()

        version = data['tag_name']
        assets = data['assets']

        for asset in assets:
            if asset['name'].endswith('.exe') and 'Windows' in asset['name']:
                return version, asset['browser_download_url'], asset['name']

        warn("No valid Windows installer found in the latest release.")
    except Exception as e:
        error(f"Failed to fetch BetterDiscord release: {e}")

    return None, None, None

def download_installer(url, name):
    """
    Downloads the BetterDiscord installer into the cache directory.
    Skips if already downloaded and valid.
    Returns the path to the installer.
    """
    CACHE_DIR.mkdir(exist_ok=True)
    dest_path = CACHE_DIR / name

    if dest_path.exists():
        info("Checking previously downloaded installer integrity...")
        try:
            expected_size = int(requests.head(url).headers.get('content-length', 0))
            actual_size = dest_path.stat().st_size
            if abs(expected_size - actual_size) > 1000:
                warn("Installer appears corrupted. Re-downloading.")
                dest_path.unlink()
            else:
                info("Installer already present and valid.")
                return dest_path
        except Exception as e:
            warn(f"Failed to validate existing installer: {e}")
            dest_path.unlink()

    info("Downloading BetterDiscord installer...")
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total = int(r.headers.get('content-length', 0))
            downloaded = 0
            chunk_size = 8192

            with open(dest_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        done = int(50 * downloaded / total) if total else 0
                        sys.stdout.write(
                            f"\r[DOWNLOAD] [{'█' * done}{'.' * (50 - done)}] "
                            f"{downloaded / 1024:.1f} / {total / 1024:.1f} KB"
                        )
                        sys.stdout.flush()

        print()  # Newline after progress bar
        info(f"Download completed: {dest_path}")
        return dest_path

    except Exception as e:
        error(f"Failed to download installer: {e}")
        return None

def run_installer(installer_path):
    """
    Runs the BetterDiscord installer silently.
    """
    info("Launching BetterDiscord setup in silent mode...")
    try:
        import subprocess
        subprocess.run([str(installer_path), "--quiet"], check=True)
        info("BetterDiscord installed successfully.")
    except subprocess.CalledProcessError as e:
        error(f"Installer exited with error: {e}")
    except Exception as e:
        error(f"Failed to run installer: {e}")