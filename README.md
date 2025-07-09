# BetterDiscord Auto-Updater

> Automatically reinstalls BetterDiscord after each Discord update — no user input needed (installer still shows UI).

![banner](https://dummyimage.com/800x180/5d3eff/ffffff&text=BetterDiscord+Auto-Updater)

---

## 🚀 Features

- Detects when Discord updates to a new version
- Automatically downloads the latest BetterDiscord installer from GitHub
- Validates the installer file (integrity check)
- Launches the installer automatically
- Restarts Discord only if it was already running
- Saves version state to skip unnecessary reinstalls
- Adds itself to Windows startup on first run
- Includes optional `--force` flag for manual reinstallation
- `.exe` conversion with icon support

---

## 🖥️ Requirements

- Windows OS
- Python 3.10+ (for source usage)

---

## 📦 Installation

You can either run the script manually or use a compiled `.exe`.

### ▶️ Option 1: Run from source

```bash
pip install -r requirements.txt
python main.py
```

> On first run, the script adds itself to Windows startup.

---

### ▶️ Option 2: Build standalone `.exe`

1. Install PyInstaller:

```bash
pip install -r dev-requirements.txt
```

2. Build the executable:

```bash
pyinstaller --noconsole --onefile --icon=icon.ico main.py
```

3. Move the generated `.exe` (from `/dist`) where you want and launch it once.

---

## ⚙️ Command-line options

| Flag      | Description                          |
|-----------|--------------------------------------|
| `--force` | Forces reinstall, even if up-to-date |

---

## 📁 Project structure

```
project_root/
├── main.py
├── config.json
├── icon.ico
├── .gitignore
├── README.md
├── LICENSE
├── requirements.txt
├── dev-requirements.txt
├── cache/
├── dist/           ← PyInstaller output
├── build/          ← PyInstaller temp
├── bd_updater/
│   ├── __init__.py
│   ├── logger.py
│   ├── updater.py
│   ├── config_utils.py
│   ├── discord_utils.py
│   ├── betterdiscord_utils.py
│   ├── autostart.py
```

---

## 🧪 Setup & Usage Commands

### 🔹 Regular users

```bash
pip install -r requirements.txt
python main.py
```

### 🔹 Developers

```bash
pip install -r dev-requirements.txt
pyinstaller --noconsole --onefile --icon=icon.ico main.py
```

---

### ✅ Summary

| Task                    | Command                                     |
|-------------------------|---------------------------------------------|
| Install runtime deps    | `pip install -r requirements.txt`           |
| Install dev tools       | `pip install -r dev-requirements.txt`       |
| Run script              | `python main.py`                            |
| Build `.exe`            | `pyinstaller --noconsole --onefile --icon=icon.ico main.py` |

---

## 📦 Downloads

Compiled executables will be provided [in the Releases section](https://github.com/Tompotio/BetterDiscord-Auto-Updater/releases) — coming soon.

---

## 👤 Author

Maintained by [Tompotio](https://github.com/Tompotio)

---

## ⚠️ Disclaimer

This project modifies Discord using third-party tooling (BetterDiscord). This may violate Discord’s Terms of Service. Use at your own risk.