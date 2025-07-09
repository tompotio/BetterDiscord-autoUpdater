import os
import sys
from pathlib import Path

def setup_autostart():
    startup_dir = Path(os.getenv("APPDATA")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    startup_dir.mkdir(parents=True, exist_ok=True)

    batch_path = startup_dir / "BetterDiscordAutoUpdater.bat"

    if getattr(sys, 'frozen', False):
        # Exécution depuis un .exe généré par PyInstaller
        target = Path(sys.executable)
    else:
        # Exécution depuis source Python
        target = f'{sys.executable}" "{Path(__file__).resolve().parents[1] / "main.py"}'

    content = f'start "" "{target}"\n'

    if batch_path.exists():
        with open(batch_path, 'r') as f:
            if content.strip() in f.read():
                return  # Déjà configuré

    with open(batch_path, 'w') as f:
        f.write(content)