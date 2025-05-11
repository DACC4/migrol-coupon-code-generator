"""
Thin wrapper around the Migrol games REST API.
Handles authentication, headers, and all HTTP calls.
"""
from typing import Dict, Optional

import requests


class MigrolApi:
    BASE_URL = "https://mmp-api.migrol.ch"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        app_installation_id: str,
        user_agent: str = "Dart/3.4 (dart:io)",
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.app_installation_id = app_installation_id
        self.user_agent = user_agent
        self._bearer_token: Optional[str] = None

    # ----------------- internal helpers -----------------

    def _request_token(self) -> str:
        url = f"{self.BASE_URL}/connect/token"
        data = {
            "grant_type": "client_credentials",
            "scope": "mmp",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        headers = {
            "User-Agent": self.user_agent,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        resp = requests.post(url, headers=headers, data=data, timeout=10)
        resp.raise_for_status()
        return resp.json()["access_token"]

    @property
    def bearer_token(self) -> str:
        if self._bearer_token is None:
            self._bearer_token = self._request_token()
        return self._bearer_token

    @property
    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.bearer_token}",
            "User-Agent": self.user_agent,
            "Accept": "application/json",
            "x-app-installation-id": self.app_installation_id,
        }

    # ----------------- public API -----------------------

    def start_game(self, game_name: str) -> Dict:
        url = f"{self.BASE_URL}/v1/games/{game_name}/start"
        resp = requests.post(url, headers=self._headers, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def end_game(self, session_id: str) -> Dict:
        url = f"{self.BASE_URL}/v1/games/end/{session_id}"
        payload = {"userInterests": ["MobilityBenzin", "EnWUnknown"]}
        resp = requests.post(url, headers=self._headers, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def game_status(self, game_name: str) -> Dict:
        endpoint = "memo" if game_name == "Memory" else game_name  # API quirk
        url = f"{self.BASE_URL}/v1/games/resources/{endpoint}"
        resp = requests.get(url, headers=self._headers, timeout=10)
        resp.raise_for_status()
        return resp.json()["playability"]
