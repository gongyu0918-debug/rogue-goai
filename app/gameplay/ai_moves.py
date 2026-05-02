from __future__ import annotations

from typing import Any, Callable, Optional

from app.config.gameplay import (
    AI_STYLE_OPTIONS,
    CPU_MAX_VISITS,
    MAX_GAME_VISITS,
    OPENING_MAX_VISITS,
    OPENING_MOVE_THRESHOLD,
    RANK_VISITS,
    ROGUE_MAX_VISITS,
    ULTIMATE_MAX_VISITS,
)


def compute_game_visits(
    level: str,
    move_count: int = -1,
    mode: str = "normal",
    *,
    cpu_mode: bool = False,
) -> int:
    raw = RANK_VISITS.get(level, 800)
    visits = MAX_GAME_VISITS if raw == 0 else min(raw, MAX_GAME_VISITS)
    if mode == "rogue":
        visits = min(visits, ROGUE_MAX_VISITS)
    elif mode == "ultimate":
        visits = min(visits, ULTIMATE_MAX_VISITS)
    if cpu_mode:
        visits = min(visits, CPU_MAX_VISITS)
    if 0 <= move_count < OPENING_MOVE_THRESHOLD and visits > OPENING_MAX_VISITS:
        visits = OPENING_MAX_VISITS
    return visits


def choose_ai_style_move(
    game: Any,
    color: str,
    top_moves: list[dict],
    style: str,
    *,
    gtp_to_coord: Callable[[str, int], Optional[tuple[int, int]]],
) -> Optional[str]:
    if style not in AI_STYLE_OPTIONS or style == "balanced":
        return None
    best_move = None
    best_score = None
    for item in top_moves[:8]:
        gtp = (item.get("move") or "").strip()
        coord = gtp_to_coord(gtp, game.size)
        if not coord:
            continue
        x, y = coord
        if game.board[y][x] != 0:
            continue
        score = _ai_style_target_score(game, color, coord, style)
        if best_score is None or score > best_score:
            best_score = score
            best_move = gtp
    return best_move


def _ai_style_target_score(game: Any, color: str, coord: tuple[int, int], style: str) -> float:
    x, y = coord
    center = (game.size - 1) / 2.0
    edge_dist = min(x, y, game.size - 1 - x, game.size - 1 - y)
    center_dist = abs(x - center) + abs(y - center)
    own = 1 if color == "B" else 2
    opp = 3 - own
    own_adj = 0
    opp_adj = 0
    for nx, ny in game.neighbors(x, y):
        cell = game.board[ny][nx]
        if cell == own:
            own_adj += 1
        elif cell == opp:
            opp_adj += 1
    if style == "territory":
        return -edge_dist * 3 + own_adj - opp_adj * 0.25
    if style == "influence":
        return -center_dist * 2 + opp_adj * 0.4
    if style == "attack":
        return opp_adj * 4 + own_adj * 0.5 - edge_dist * 0.3
    if style == "defense":
        return own_adj * 4 + opp_adj * 0.2 - center_dist * 0.2
    return 0.0
