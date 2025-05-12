"""
Handles all persistence for coupons:
  • <dir>/<ean>.json   - pretty-printed metadata
  • <dir>/<ean>.png    - EAN-13 barcode
"""
import json
import os
from typing import Dict

from barcode import EAN13
from barcode.writer import ImageWriter


class CouponManager:
    def __init__(self, directory: str = "coupons") -> None:
        self.directory = directory
        os.makedirs(directory, exist_ok=True)

    def save(self, coupon: Dict) -> str:
        """
        Writes JSON and PNG, then returns the PNG path (for Telegram).
        """
        ean = coupon["eanCode"]
        json_path = os.path.join(self.directory, f"{ean}.json")
        png_path = os.path.join(self.directory, f"{ean}.png")

        # JSON metadata
        with open(json_path, "w") as fp:
            json.dump(coupon, fp, indent=4)

        # Barcode image
        with open(png_path, "wb") as img:
            EAN13(str(ean), writer=ImageWriter()).write(img)

        return png_path
