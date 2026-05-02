from __future__ import annotations

from typing import Any


def reset_ultimate_effect_state(game: Any) -> None:
    game.ultimate_joseki_targets = []
    game.ultimate_joseki_hits = 0
    game.ultimate_joseki_done = False
    game.ultimate_godhand_center = None
    game.ultimate_godhand_trigger = []
    game.ultimate_godhand_done = False
    game.ultimate_corner_helper_done = set()
    game.ultimate_sanrensei_done = False
    game.ultimate_five_in_row_seen = set()
    game.ultimate_last_stand_done = {"B": False, "W": False}
    game.ultimate_quickthink_active = False
    game.ultimate_quickthink_turn_counted = False
    game.ultimate_fool_shapes = set()
    game.ultimate_shadow_clone_links = []
