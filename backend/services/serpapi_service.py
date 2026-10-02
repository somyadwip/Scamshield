"""SerpApi service – thin wrapper around the official client.

Handles authentication, rate limits, timeouts, and error translation.
"""

from __future__ import annotations

import logging
import os
from typing import Any

from serpapi import GoogleSearch

logger = logging.getLogger("scamshield.serpapi")

# Number of organic results requested per query (keeps quota low)
RESULTS_PER_QUERY = 8


class SerpApiError(Exception):
    """Raised when SerpApi returns an error."""

    def __init__(self, message: str, error_type: str = "serpapi_error"):
        self.message = message
        self.error_type = error_type
        super().__init__(message)


class SerpApiService:
    """Stateless wrapper around the SerpApi Google Search endpoint."""

    @property
    def api_key(self) -> str:
        # Dynamically reload .env so user edits take effect immediately
        from dotenv import load_dotenv
        load_dotenv(override=True)
        return os.getenv("SERPAPI_KEY", "").strip()

    # ── Public helpers ──────────────────────────────────────────────────────

    def is_configured(self) -> bool:
        """Return True when an API key is present and not the placeholder."""
        key = self.api_key
        return bool(key) and key != "PASTE_YOUR_SERPAPI_KEY_HERE"

    def search(self, query: str, *, num: int = RESULTS_PER_QUERY) -> dict[str, Any]:
        """Run a single Google search via SerpApi.

        Returns the raw JSON dict from SerpApi.
        Raises SerpApiError on any failure.
        """
        if not self.is_configured():
            raise SerpApiError(
                "SerpApi key is not configured. Please add your key to backend/.env",
                error_type="api_key_missing",
            )

        try:
            params = {
                "engine": "google",
                "q": query,
                "num": num,
                "api_key": self.api_key,
            }
            search = GoogleSearch(params)
            results = search.get_dict()

            # Check for SerpApi-level errors
            if "error" in results:
                error_msg = results["error"]
                if "Invalid API key" in str(error_msg) or "Wrong API" in str(error_msg):
                    raise SerpApiError(str(error_msg), error_type="invalid_api_key")
                if "rate" in str(error_msg).lower():
                    raise SerpApiError(str(error_msg), error_type="rate_limit")
                raise SerpApiError(str(error_msg))

            return results

        except SerpApiError:
            raise
        except Exception as exc:
            logger.exception("SerpApi search failed for query: %s", query)
            raise SerpApiError(
                f"Search failed: {exc!s}",
                error_type="search_error",
            ) from exc

    def search_news(self, query: str, *, num: int = 5) -> dict[str, Any]:
        """Run a Google News search via SerpApi."""
        if not self.is_configured():
            raise SerpApiError(
                "SerpApi key is not configured. Please add your key to backend/.env",
                error_type="api_key_missing",
            )

        try:
            params = {
                "engine": "google",
                "q": query,
                "tbm": "nws",
                "num": num,
                "api_key": self.api_key,
            }
            search = GoogleSearch(params)
            results = search.get_dict()
            if "error" in results:
                raise SerpApiError(str(results["error"]))
            return results
        except SerpApiError:
            raise
        except Exception as exc:
            logger.exception("SerpApi news search failed for query: %s", query)
            raise SerpApiError(f"News search failed: {exc!s}") from exc


# Singleton – import and reuse
serpapi_service = SerpApiService()
