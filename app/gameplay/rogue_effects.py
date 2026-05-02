from __future__ import annotations

import random
from typing import Any

from app.config.gameplay import (
    CHALLENGE_ACTIVE_USE_BONUS,
    CHALLENGE_DERIVATIVE_BONUS_CHANCE,
    CHALLENGE_SET_MIN_COUNT,
    CHALLENGE_ZONE_EXPAND_RADIUS,
)
from app.data.cards import challenge_card_category, challenge_category_counts


def reset_rogue_effect_state(
    game: Any,
    *,
    reset_uses: bool = False,
    reset_handicap: bool = False,
) -> None:
    if reset_uses:
        game.rogue_uses = {}
    game.rogue_waiting_seal = False
    game.rogue_skip_ai = False
    game.rogue_joseki_targets = []
    game.rogue_joseki_hits = 0
    game.rogue_joseki_done = False
    game.rogue_godhand_center = None
    game.rogue_godhand_trigger = []
    game.rogue_godhand_done = False
    game.rogue_sansan_trap_done = False
    game.rogue_corner_helper_done = set()
    game.rogue_sanrensei_done = False
    game.rogue_puppet_target = None
    game.rogue_five_in_row_seen = set()
    game.rogue_last_stand_done = {"B": False, "W": False}
    game.rogue_capture_foul_progress = {"B": 0, "W": 0}
    game.rogue_coach_moves_left = 0
    game.rogue_coach_bonus_checked = False
    game.rogue_quickthink_stage = 0
    game.rogue_fool_shapes = set()
    game.rogue_seal_points = []
    if reset_handicap:
        game.rogue_handicap_passes = 0
        game.rogue_handicap_active = False
        game.rogue_handicap_bonuses = 0


def apply_rogue_card_uses(game: Any, card_id: str, card_def: dict[str, Any], *, bonus: int = 0) -> None:
    if "uses" in card_def:
        game.rogue_uses[card_id] = card_def["uses"] + bonus


def rogue_card_ids(game: Any) -> list[str]:
    cards: list[str] = []
    for card_id in list(getattr(game, "challenge_cards", [])) + [game.rogue_card]:
        if card_id and card_id not in cards:
            cards.append(card_id)
    return cards


def rogue_has(game: Any, card_id: str) -> bool:
    return card_id in rogue_card_ids(game)


def challenge_remaining(game: Any, key: str) -> int:
    return max(0, game.challenge_limits.get(key, 0) - game.challenge_usage.get(key, 0))


def challenge_category_counts_for_game(game: Any) -> dict[str, int]:
    return challenge_category_counts(list(getattr(game, "challenge_cards", [])))


def challenge_has_set(
    game: Any,
    category: str,
    need: int = CHALLENGE_SET_MIN_COUNT,
) -> bool:
    if not getattr(game, "challenge_beta", False):
        return False
    return challenge_category_counts_for_game(game).get(category, 0) >= need


def challenge_zone_points(game: Any, points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not challenge_has_set(game, "zone"):
        return list(points)
    expanded: set[tuple[int, int]] = set()
    for px, py in points:
        for dy in range(-CHALLENGE_ZONE_EXPAND_RADIUS, CHALLENGE_ZONE_EXPAND_RADIUS + 1):
            for dx in range(-CHALLENGE_ZONE_EXPAND_RADIUS, CHALLENGE_ZONE_EXPAND_RADIUS + 1):
                nx, ny = px + dx, py + dy
                if 0 <= nx < game.size and 0 <= ny < game.size:
                    expanded.add((nx, ny))
    return sorted(expanded)


def challenge_active_use_bonus(game: Any, card_id: str) -> int:
    if not challenge_has_set(game, "active"):
        return 0
    return CHALLENGE_ACTIVE_USE_BONUS if challenge_card_category(card_id) == "active" else 0


def challenge_should_bonus_derivative(game: Any) -> bool:
    return (
        challenge_has_set(game, "derivative")
        and random.random() < CHALLENGE_DERIVATIVE_BONUS_CHANCE
    )
