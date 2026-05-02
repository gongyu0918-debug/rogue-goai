from __future__ import annotations

import random
from collections.abc import Awaitable
from dataclasses import dataclass
from typing import Any, Callable, Optional

import app.config.gameplay as gameplay_config


@dataclass(frozen=True)
class AiMovePlan:
    mode: str
    effective_level: str
    visits: int
    time_limit: float
    move_count: int
    ai_move_count: int


def compute_game_visits(
    level: str,
    move_count: int = -1,
    mode: str = "normal",
    *,
    cpu_mode: bool = False,
) -> int:
    raw = gameplay_config.RANK_VISITS.get(level, 800)
    visits = gameplay_config.MAX_GAME_VISITS if raw == 0 else min(raw, gameplay_config.MAX_GAME_VISITS)
    if mode == "rogue":
        visits = min(visits, gameplay_config.ROGUE_MAX_VISITS)
    elif mode == "ultimate":
        visits = min(visits, gameplay_config.ULTIMATE_MAX_VISITS)
    if cpu_mode:
        visits = min(visits, gameplay_config.CPU_MAX_VISITS)
    if (
        0 <= move_count < gameplay_config.OPENING_MOVE_THRESHOLD
        and visits > gameplay_config.OPENING_MAX_VISITS
    ):
        visits = gameplay_config.OPENING_MAX_VISITS
    return visits


def plan_rogue_ai_search(
    game: Any,
    rogue_cards: set[str],
    *,
    move_count: int,
    ai_move_count: int,
    get_game_visits: Callable[[str, int, str], int],
    weaken_rank: Callable[[str, int], str],
) -> AiMovePlan:
    mode = "rogue" if rogue_cards else "normal"
    effective_level = game.level
    if "nerf" in rogue_cards:
        effective_level = weaken_rank(effective_level, 8)
    if "time_press" in rogue_cards:
        effective_level = weaken_rank(effective_level, 5)
    visits = get_game_visits(effective_level, move_count, mode)

    if "nerf" in rogue_cards:
        visits = max(30, int(visits * gameplay_config.ROGUE_NERF_FACTOR))

    if move_count < gameplay_config.OPENING_MOVE_THRESHOLD:
        time_limit = min(3.0, gameplay_config.MAX_MOVE_TIME)
    elif visits > 5000:
        time_limit = gameplay_config.MAX_MOVE_TIME
    else:
        time_limit = 8.0

    if "time_press" in rogue_cards:
        time_limit = min(gameplay_config.ROGUE_TIME_PRESS_MAX_TIME, time_limit)
        visits = min(visits, gameplay_config.ROGUE_TIME_PRESS_MAX_VISITS)

    return AiMovePlan(
        mode=mode,
        effective_level=effective_level,
        visits=visits,
        time_limit=time_limit,
        move_count=move_count,
        ai_move_count=ai_move_count,
    )


def choose_ai_style_move(
    game: Any,
    color: str,
    top_moves: list[dict],
    style: str,
    *,
    gtp_to_coord: Callable[[str, int], Optional[tuple[int, int]]],
) -> Optional[str]:
    if style not in gameplay_config.AI_STYLE_OPTIONS or style == "balanced":
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


class AiMoveService:
    def __init__(
        self,
        *,
        engine: Any,
        run_in_executor: Callable[..., Awaitable[Any]],
        engine_log: Callable[[str], None],
        coord_to_gtp: Callable[[int, int, int], str],
        gtp_to_coord: Callable[[str, int], Optional[tuple[int, int]]],
    ) -> None:
        self._engine = engine
        self._run_in_executor = run_in_executor
        self._engine_log = engine_log
        self._coord_to_gtp = coord_to_gtp
        self._gtp_to_coord = gtp_to_coord

    async def pick_nonpass_fallback_move(
        self,
        game: Any,
        color: str,
        visits: int,
        forbidden: Optional[set[tuple[int, int]]] = None,
    ) -> Optional[str]:
        forbidden = forbidden or set()
        try:
            lines, _ = self._engine.analyze(
                color,
                visits=max(100, min(visits, 1200)),
                interval=50,
                duration=1.5,
                extra_args=["rootInfo", "true"],
            )
            result = self._engine.parse_analysis(lines, [], game.size, to_move_color=color)
            for item in result.get("top_moves", []):
                gtp = (item.get("move") or item.get("gtp") or "").strip()
                if not gtp or gtp.upper() in {"PASS", "RESIGN"}:
                    continue
                coord = self._gtp_to_coord(gtp, game.size)
                if not coord or game.board[coord[1]][coord[0]] != 0:
                    continue
                if coord in forbidden or not game.is_legal_move(coord[0], coord[1], color):
                    continue
                with self._engine.command_lock:
                    resp = self._engine._send_command_locked(f"play {color} {gtp}")
                    if "?" not in resp:
                        return gtp
        except Exception as exc:
            self._engine_log(f"non-pass fallback failed: {exc}")
        return None

    async def pick_ranked_legal_move(
        self,
        game: Any,
        color: str,
        visits: int,
        forbidden: Optional[set[tuple[int, int]]] = None,
        *,
        time_limit: float = 1.5,
    ) -> Optional[str]:
        forbidden = forbidden or set()
        try:
            lines, _ = await self._run_in_executor(
                self._engine.analyze,
                color,
                max(120, min(visits, 1400)),
                50,
                time_limit,
                ["rootInfo", "true"],
            )
            result = self._engine.parse_analysis(lines, [], game.size, to_move_color=color)
            candidates = []
            for item in result.get("top_moves", []):
                gtp = (item.get("move") or item.get("gtp") or "").strip()
                if not gtp or gtp.upper() in {"PASS", "RESIGN"}:
                    continue
                coord = self._gtp_to_coord(gtp, game.size)
                if (
                    coord
                    and coord not in forbidden
                    and game.board[coord[1]][coord[0]] == 0
                    and game.is_legal_move(coord[0], coord[1], color)
                ):
                    candidates.append(gtp)
            for gtp in candidates:
                with self._engine.command_lock:
                    resp = self._engine._send_command_locked(f"play {color} {gtp}")
                    if "?" not in resp:
                        return gtp
        except Exception as exc:
            self._engine_log(f"ranked legal fallback failed: {exc}")
        return None

    async def avoid_points(
        self,
        game: Any,
        color: str,
        visits: int,
        time_limit: float,
        forbidden: list[tuple[int, int]] | set[tuple[int, int]],
    ) -> str:
        forbidden_gtp = {
            self._coord_to_gtp(x, y, game.size)
            for x, y in forbidden
        }
        forbidden_gtp_upper = {s.upper() for s in forbidden_gtp}
        forbidden_coords = set(forbidden)

        def _analyze_and_pick():
            with self._engine.command_lock:
                mv = 10000000 if visits == 0 else visits
                self._engine._send_command_locked(f"kata-set-param maxVisits {mv}")
                self._engine.current_visits = visits
                self._engine._send_command_locked(f"kata-set-param maxTime {time_limit}")
                resp = self._engine._send_command_locked(
                    f"genmove {color}",
                    timeout=max(60, time_limit + 15),
                )
                self._engine._send_command_locked("kata-set-param maxTime -1")

                gtp_move = resp.replace("=", "").strip()
                if (
                    gtp_move.upper() not in ("PASS", "RESIGN")
                    and gtp_move.upper() not in forbidden_gtp_upper
                ):
                    return gtp_move

                if gtp_move.upper() not in ("PASS", "RESIGN"):
                    self._engine._send_command_locked("undo")
                for attempt in range(5):
                    v = max(50, visits // (2 + attempt))
                    self._engine._send_command_locked(f"kata-set-param maxVisits {v}")
                    resp2 = self._engine._send_command_locked(f"genmove {color}", timeout=20)
                    m = resp2.replace("=", "").strip()
                    if (
                        m.upper() not in ("PASS", "RESIGN")
                        and m.upper() not in forbidden_gtp_upper
                    ):
                        return m
                    if m.upper() not in ("PASS", "RESIGN"):
                        self._engine._send_command_locked("undo")
                return None

        picked = await self._run_in_executor(_analyze_and_pick)
        if picked:
            return picked

        ranked = await self.pick_ranked_legal_move(
            game,
            color,
            visits,
            forbidden_coords,
            time_limit=1.3,
        )
        if ranked:
            return ranked

        def _last_resort():
            with self._engine.command_lock:
                allowed = [
                    (x, y)
                    for y in range(game.size) for x in range(game.size)
                    if game.board[y][x] == 0
                    and (x, y) not in forbidden_coords
                    and game.is_legal_move(x, y, color)
                ]
                random.shuffle(allowed)
                for ax, ay in allowed:
                    gtp = self._coord_to_gtp(ax, ay, game.size)
                    r = self._engine._send_command_locked(f"play {color} {gtp}")
                    if "?" not in r:
                        return gtp
                self._engine._send_command_locked(f"play {color} pass")
                return "pass"

        return await self._run_in_executor(_last_resort)

    async def allow_only_points(
        self,
        game: Any,
        color: str,
        visits: int,
        time_limit: float,
        allowed: list[tuple[int, int]],
    ) -> str:
        allowed_gtp = {self._coord_to_gtp(x, y, game.size).upper() for x, y in allowed}

        def _pick():
            with self._engine.command_lock:
                mv = max(50, min(visits, 2000))
                self._engine._send_command_locked(f"kata-set-param maxVisits {mv}")
                self._engine.current_visits = mv
                self._engine._send_command_locked(
                    f"kata-set-param maxTime {min(time_limit, 3.0)}"
                )

                for attempt in range(6):
                    v = max(50, mv // (1 + attempt))
                    self._engine._send_command_locked(f"kata-set-param maxVisits {v}")
                    resp = self._engine._send_command_locked(f"genmove {color}", timeout=15)
                    m = resp.replace("=", "").strip()
                    if m.upper() in ("PASS", "RESIGN"):
                        self._engine._send_command_locked("kata-set-param maxTime -1")
                        return m
                    if m.upper() in allowed_gtp:
                        self._engine._send_command_locked("kata-set-param maxTime -1")
                        return m
                    self._engine._send_command_locked("undo")

                self._engine._send_command_locked("kata-set-param maxTime -1")
                random.shuffle(allowed)
                for ax, ay in allowed:
                    if game.board[ay][ax] == 0:
                        gtp = self._coord_to_gtp(ax, ay, game.size)
                        r = self._engine._send_command_locked(f"play {color} {gtp}")
                        if "?" not in r:
                            return gtp
                resp = self._engine._send_command_locked(f"genmove {color}", timeout=15)
                return resp.replace("=", "").strip()

        return await self._run_in_executor(_pick)

    async def suboptimal_move(
        self,
        game: Any,
        color: str,
        visits: int,
        time_limit: float,
        start_idx: int = 2,
        end_idx: int = 5,
    ) -> Optional[str]:
        del time_limit

        def _analyze_pick():
            mv = max(200, min(visits, 3000))
            lines, _ = self._engine.analyze(
                color,
                visits=mv,
                interval=50,
                duration=2.0,
                extra_args=["rootInfo", "true"],
            )
            result = self._engine.parse_analysis(lines, [], game.size, to_move_color=color)

            top = result.get("top_moves", [])
            if len(top) < end_idx:
                return None

            pick = random.choice(top[start_idx:end_idx])
            gtp = pick.get("move") or pick.get("gtp")
            if not gtp:
                return None

            with self._engine.command_lock:
                resp = self._engine._send_command_locked(f"play {color} {gtp}")
                if "?" in resp:
                    return None
            return gtp

        return await self._run_in_executor(_analyze_pick)

    async def no_resign_move(self, game: Any, color: str) -> str:
        del game

        def _retry():
            with self._engine.command_lock:
                for v in (100, 30, 10):
                    self._engine._send_command_locked(f"kata-set-param maxVisits {v}")
                    self._engine._send_command_locked("kata-set-param maxTime 2")
                    resp = self._engine._send_command_locked(f"genmove {color}", timeout=10)
                    self._engine._send_command_locked("kata-set-param maxTime -1")
                    m = resp.replace("=", "").strip()
                    if m.upper() != "RESIGN":
                        return m
                    self._engine._send_command_locked("undo")
                self._engine._send_command_locked(f"play {color} pass")
                return "pass"

        return await self._run_in_executor(_retry)

    async def retry_avoiding_ko(self, game: Any, color: str) -> str:
        def _retry():
            with self._engine.command_lock:
                self._engine._send_command_locked("undo")

                for attempt in range(5):
                    v = max(50, 800 // (2 + attempt))
                    self._engine._send_command_locked(f"kata-set-param maxVisits {v}")
                    self._engine._send_command_locked("kata-set-param maxTime 3")
                    resp = self._engine._send_command_locked(f"genmove {color}", timeout=10)
                    self._engine._send_command_locked("kata-set-param maxTime -1")
                    m = resp.replace("=", "").strip()
                    if m.upper() in ("PASS", "RESIGN"):
                        return m
                    coord = self._gtp_to_coord(m, game.size)
                    if not coord or not game.is_ko(coord[0], coord[1], color):
                        return m
                    self._engine._send_command_locked("undo")

                empties = [
                    (x, y)
                    for y in range(game.size) for x in range(game.size)
                    if game.board[y][x] == 0
                    and game.is_legal_move(x, y, color)
                ]
                random.shuffle(empties)
                for ax, ay in empties:
                    gtp = self._coord_to_gtp(ax, ay, game.size)
                    r = self._engine._send_command_locked(f"play {color} {gtp}")
                    if "?" not in r:
                        return gtp

                self._engine._send_command_locked(f"play {color} pass")
                return "pass"

        return await self._run_in_executor(_retry)
