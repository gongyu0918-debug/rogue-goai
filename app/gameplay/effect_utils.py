from __future__ import annotations

import random
import time
from typing import Any, Optional


def get_star_points(size: int) -> list[tuple[int, int]]:
    if size == 19:
        return [
            (3, 3), (9, 3), (15, 3), (3, 9), (9, 9), (15, 9),
            (3, 15), (9, 15), (15, 15),
        ]
    if size == 13:
        return [
            (3, 3), (6, 3), (9, 3), (3, 6), (6, 6), (9, 6),
            (3, 9), (6, 9), (9, 9),
        ]
    if size == 9:
        return [
            (2, 2), (4, 2), (6, 2), (2, 4), (4, 4), (6, 4),
            (2, 6), (4, 6), (6, 6),
        ]
    c = size // 2
    return [(c, c)]


def get_blackhole_points(size: int) -> list[tuple[int, int]]:
    c = size // 2
    pts = []
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            if abs(dx) + abs(dy) <= 2:
                nx, ny = c + dx, c + dy
                if 0 <= nx < size and 0 <= ny < size:
                    pts.append((nx, ny))
    return pts


def get_golden_corner_points(size: int, corner: int, span: int = 5) -> list[tuple[int, int]]:
    pts = []
    for dy in range(span):
        for dx in range(span):
            if corner == 0:
                pts.append((dx, dy))
            elif corner == 1:
                pts.append((size - 1 - dx, dy))
            elif corner == 2:
                pts.append((dx, size - 1 - dy))
            else:
                pts.append((size - 1 - dx, size - 1 - dy))
    return pts


def get_sansan_points(size: int) -> list[tuple[int, int]]:
    return [(2, 2), (size - 3, 2), (2, size - 3), (size - 3, size - 3)]


def pick_joseki_targets(size: int, n: int = 8) -> list[tuple[int, int]]:
    rng = random.Random(time.time_ns())
    offsets = [(2, 2), (2, 3), (3, 2), (3, 3), (2, 4), (4, 2), (3, 4), (4, 3)]
    candidates = []
    for bx in (0, size - 1):
        for by in (0, size - 1):
            for ox, oy in offsets:
                x = ox if bx == 0 else size - 1 - ox
                y = oy if by == 0 else size - 1 - oy
                if 0 <= x < size and 0 <= y < size:
                    candidates.append((x, y))
    candidates = list(dict.fromkeys(candidates))
    rng.shuffle(candidates)
    return candidates[:n]


def is_lowline(x: int, y: int, size: int) -> bool:
    return x <= 2 or x >= size - 3 or y <= 2 or y >= size - 3


def mirror_coord(x: int, y: int, size: int) -> tuple[int, int]:
    return size - 1 - x, size - 1 - y


def adjacent_points(x: int, y: int, size: int) -> list[tuple[int, int]]:
    pts = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < size and 0 <= ny < size:
            pts.append((nx, ny))
    return pts


def adjacent8_points(x: int, y: int, size: int) -> list[tuple[int, int]]:
    pts = []
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size:
                pts.append((nx, ny))
    return pts


def diamond_points(
    cx: int,
    cy: int,
    radius: int,
    size: int,
    *,
    boundary_only: bool = False,
    include_center: bool = True,
) -> list[tuple[int, int]]:
    pts = []
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            dist = abs(dx) + abs(dy)
            if dist > radius:
                continue
            if boundary_only and dist != radius:
                continue
            if not include_center and dist == 0:
                continue
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < size and 0 <= ny < size:
                pts.append((nx, ny))
    return pts


def get_square_points(cx: int, cy: int, radius: int, size: int) -> list[tuple[int, int]]:
    pts = []
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < size and 0 <= ny < size:
                pts.append((nx, ny))
    return pts


def random_hidden_center(size: int, radius: int, rng: random.Random) -> tuple[int, int]:
    low = max(radius, 0)
    high = max(low, size - radius - 1)
    return rng.randint(low, high), rng.randint(low, high)


def line_key(points: list[tuple[int, int]] | tuple[tuple[int, int], ...]) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(points))


def find_exact_five_lines(game: Any, color: str) -> list[tuple[tuple[int, int], ...]]:
    cv = 1 if color == "B" else 2
    lines = []
    seen = set()
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for y in range(game.size):
        for x in range(game.size):
            if game.board[y][x] != cv:
                continue
            for dx, dy in directions:
                px, py = x - dx, y - dy
                if 0 <= px < game.size and 0 <= py < game.size and game.board[py][px] == cv:
                    continue
                run = []
                cx, cy = x, y
                while 0 <= cx < game.size and 0 <= cy < game.size and game.board[cy][cx] == cv:
                    run.append((cx, cy))
                    cx += dx
                    cy += dy
                if len(run) != 5:
                    continue
                key = line_key(run)
                if key in seen:
                    continue
                seen.add(key)
                lines.append(key)
    return lines


def line_endpoints(
    line: tuple[tuple[int, int], ...],
) -> tuple[Optional[tuple[int, int]], Optional[tuple[int, int]]]:
    if len(line) != 5:
        return None, None
    sorted_line = sorted(line)
    x1, y1 = sorted_line[0]
    x2, y2 = sorted_line[1]
    dx, dy = x2 - x1, y2 - y1
    return (x1 - dx, y1 - dy), (sorted_line[-1][0] + dx, sorted_line[-1][1] + dy)


def line_points_between(x1: int, y1: int, x2: int, y2: int) -> list[tuple[int, int]]:
    pts: list[tuple[int, int]] = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    x, y = x1, y1
    while True:
        pts.append((x, y))
        if x == x2 and y == y2:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
    return pts


def count_stones(game: Any, color_val: int) -> int:
    return sum(cell == color_val for row in game.board for cell in row)
