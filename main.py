import argparse
from bd_updater.autostart import setup_autostart
from bd_updater.updater import perform_update

def main():
    setup_autostart()
    
    parser = argparse.ArgumentParser(description="BetterDiscord Auto-Updater")
    parser.add_argument("--force", action="store_true", help="Force reinstall even if versions are unchanged")
    args = parser.parse_args()

    perform_update(force=args.force)

if __name__ == "__main__":
    main()