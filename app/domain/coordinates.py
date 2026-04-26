from __future__ import annotations


GTP_COLUMNS = "ABCDEFGHJKLMNOPQRST"


def coord_to_gtp(x: int, y: int, size: int = 19) -> str:
    """Convert zero-based board coordinates to GTP notation."""
    return f"{GTP_COLUMNS[x]}{size - y}"


def gtp_to_coord(gtp: str, size: int = 19) -> tuple[int, int] | None:
    """Convert GTP notation to zero-based board coordinates."""
    if gtp.upper() == "PASS":
        return None
    try:
        col = GTP_COLUMNS.index(gtp[0].upper())
        row = size - int(gtp[1:])
        if 0 <= col < size and 0 <= row < size:
            return col, row
    except (ValueError, IndexError):
        print(f"[GTP] Invalid coord: {gtp!r}")
    return None

