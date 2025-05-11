import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from src.coupon_manager import CouponManager
from src.game_runner import GameRunner
from src.migrol_api import MigrolApi
from src.telegram_notifier import TelegramNotifier


def main() -> None:
    load_dotenv()

    # Migrol creds
    client_secret = os.getenv("CLIENT_SECRET")
    app_installation_id = os.getenv("APP_INSTALLATION_ID")
    if not client_secret or not app_installation_id:
        raise RuntimeError(
            "Set CLIENT_SECRET and APP_INSTALLATION_ID in the "
            "environment or .env file."
        )

    # Telegram creds (optional - handled in TelegramNotifier)
    try:
        notifier = TelegramNotifier()
    except RuntimeError as err:
        print(f"🛈 Telegram disabled: {err}")
        notifier = None

    api = MigrolApi(
        client_id="migrol-app",
        client_secret=client_secret,
        app_installation_id=app_installation_id,
    )
    coupon_manager = CouponManager()
    games = ["Memory", "HalfMatching"]

    GameRunner(api, coupon_manager, games, notifier=notifier).run()

if __name__ == "__main__":
    main()
