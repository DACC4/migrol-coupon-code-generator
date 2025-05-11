"""
Sends coupons to a Telegram chat via *python-telegram-bot* ≥ v20.

Required env vars (unless passed explicitly):
  • TELEGRAM_BOT_TOKEN
  • TELEGRAM_CHAT_ID
"""
from __future__ import annotations

import asyncio
import os
from typing import Optional

from telegram import Bot
from telegram.constants import ParseMode


class TelegramNotifier:
    def __init__(
        self,
        bot_token: Optional[str] = None,
        chat_id: Optional[str] = None,
    ) -> None:
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")

        if not self.bot_token or not self.chat_id:
            raise RuntimeError(
                "TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set "
                "in the environment or passed to TelegramNotifier()."
            )

        self.bot = Bot(token=self.bot_token)

    # ------------------------------------------------------------------ #
    # synchronous wrapper – keeps the rest of the codebase unchanged
    # ------------------------------------------------------------------ #
    def send_coupon(
        self,
        title: str,
        ean_code: str,
        expiration_date: str,
        image_path: str,
    ) -> None:
        """
        Fire-and-forget helper so caller can stay synchronous.
        """
        asyncio.run(
            self._send_photo_async(title, ean_code, expiration_date, image_path)
        )

    # ------------------------------------------------------------------ #
    # async implementation
    # ------------------------------------------------------------------ #
    async def _send_photo_async(
        self,
        title: str,
        ean_code: str,
        expiration_date: str,
        image_path: str,
    ) -> None:
        caption = (
            f"🎁 *{title}*\n"
            f"🔢 `EAN: {ean_code}`\n"
            f"📅 *Valid until:* {expiration_date}\n"
            "Happy saving! 🛍️"
        )

        async with self.bot:
            with open(image_path, "rb") as img:
                await self.bot.send_photo(
                    chat_id=self.chat_id,
                    photo=img,
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN,
                )
