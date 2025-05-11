"""
High-level orchestration:
 • checks daily limits
 • plays remaining attempts
 • passes coupons to CouponManager (and optionally Telegram)
"""
from typing import Dict, List, Optional

from .coupon_manager import CouponManager
from .migrol_api import MigrolApi
from .telegram_notifier import TelegramNotifier


class GameRunner:
    def __init__(
        self,
        api: MigrolApi,
        coupon_manager: CouponManager,
        games: List[str],
        notifier: Optional[TelegramNotifier] = None,
    ) -> None:
        self.api = api
        self.coupon_manager = coupon_manager
        self.games = games
        self.notifier = notifier

    # --------------------------------------------------------------------- #

    def run(self) -> None:
        for game in self.games:
            self._play_if_possible(game)

    # ---------------- internal helpers ----------------------------------- #

    def _play_if_possible(self, game: str) -> None:
        print(f"🔍 Checking status for {game}…")
        status = self.api.game_status(game)
        allowed = status["allowedAttemptsPerDay"]
        played = status["timesPlayedToday"]

        if played >= allowed:
            print(f"⏭  Limit reached for {game} ({played}/{allowed}).")
            return

        for attempt in range(allowed - played):
            print(f"🎮 {game}: attempt {played + attempt + 1}/{allowed}")
            session_id = self.api.start_game(game)["gameSessionId"]
            result = self.api.end_game(session_id)
            self._maybe_save_and_notify(result)

    # --------------------------------------------------------------------- #

    def _maybe_save_and_notify(self, result: Dict) -> None:
        coupon_blob = result.get("coupon")
        if not coupon_blob:
            print("…no coupon this round.")
            return

        title = next(
            (
                entry["title"]
                for entry in coupon_blob.get("content", [])
                if entry.get("language") == "EN"
            ),
            "Unknown coupon",
        )

        coupon = {
            "eanCode": coupon_blob["eanCode"],
            "expirationDate": coupon_blob["validUntil"],
            "title": title,
        }
        print(f"💰  Coupon received: {title} (EAN {coupon['eanCode']})")

        # Save locally → returns PNG path
        png_path = self.coupon_manager.save(coupon)

        # Telegram
        if self.notifier:
            try:
                self.notifier.send_coupon(
                    title=coupon["title"],
                    ean_code=coupon["eanCode"],
                    expiration_date=coupon["expirationDate"],
                    image_path=png_path,
                )
                print("📤  Sent to Telegram.")
            except Exception as exc:  # noqa: BLE001
                # we don't want Telegram hiccups to crash the run
                print(f"⚠️  Telegram send failed: {exc}")
