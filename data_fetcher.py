import logging
from typing import Dict, Optional

import requests

from config import API_KEY, API_HOST

logger = logging.getLogger(__name__)

BASE_URL = f"https://{API_HOST}"


def _request(endpoint: str, params: dict | None = None) -> dict:
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST,
    }
    url = f"{BASE_URL}/{endpoint}"
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:  # broad catch to log any issue
        logger.error("API request failed: %s", exc)
        return {}


def buscar_id_jogador(nome: str) -> Optional[int]:
    """Return the first player ID that matches the provided name."""
    data = _request("tennis/v2/search", {"search": nome})
    players = (
        data.get("players")
        or data.get("results")
        or []
    )
    for player in players:
        player_id = player.get("id") or player.get("playerId")
        if player_id:
            return player_id
    logger.info("No player found for name '%s'", nome)
    return None


def buscar_stats_por_piso(player_id: int) -> Dict[str, Dict[str, int]]:
    """Fetch win/loss statistics by surface for a player."""
    data = _request(f"tennis/v2/atp/player/surface-summary/{player_id}")
    stats = {}
    # The actual structure may vary; try to be defensive.
    surfaces = (
        data.get("player", {}).get("surfaceStats")
        or data.get("surfaces")
        or data.get("surfaceSummaries")
        or []
    )
    for item in surfaces:
        surface = item.get("surface") or item.get("name")
        if not surface:
            continue
        stats[surface.lower()] = {
            "wins": item.get("wins") or item.get("win"),
            "losses": item.get("losses") or item.get("loss"),
        }
    return stats


def buscar_stats_jogador(nome: str) -> Optional[Dict[str, Dict[str, int]]]:
    player_id = buscar_id_jogador(nome)
    if player_id is None:
        return None
    return buscar_stats_por_piso(player_id)

