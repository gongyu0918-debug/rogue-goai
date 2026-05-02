from __future__ import annotations

from typing import Any


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
