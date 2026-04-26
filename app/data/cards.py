"""Card definitions and related pure data."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

ROGUE_CARDS = {
    "tengen": {"name": "天元", "desc": "开局 5 手，AI 会优先靠近天元与星位落子", "icon": "◎"},
    "dice": {"name": "掷骰", "desc": "AI 每手有 10% 概率直接虚手", "icon": "🎉"},
    "erosion": {"name": "蚕食", "desc": "每提 1 子，贴目向有利方偏移 4 目", "icon": "🌑"},
    "puppet": {"name": "傀儡术", "desc": "先选定 AI 下一手的落点；你先正常落子，随后 AI 会被迫下在那里（限 1 次）", "icon": "🎁", "uses": 1},
    "seal": {"name": "封印术", "desc": "指定 4 个禁着点，整局 AI 都不能下在这些点", "icon": "🔀"},
    "twin": {"name": "连击", "desc": "本回合可连续落两手（限 1 次）", "icon": "✦", "uses": 1},
    "nerf": {"name": "弱化", "desc": "AI 大约下降 8 段，搜索算力只剩约 5%，前 12 手更容易误选备选点", "icon": "📲"},
    "komi_relief": {"name": "贴目减半", "desc": "贴目会朝你有利的方向调整 7 目", "icon": "✘️"},
    "time_press": {"name": "限时压制", "desc": "AI 大约下降 5 段，且每手最多思考 0.10 秒，前 12 手更容易仓促误判", "icon": "⏱️"},
    "lowline": {"name": "低空飞行", "desc": "AI 前 8 手偏向二三路低位", "icon": "🦊"},
    "suboptimal": {"name": "次优之选", "desc": "AI 前 8 手更容易从后几名的候选点里随机挑一手", "icon": "🚍"},
    "mirror": {"name": "镜像", "desc": "AI 有 16% 概率按棋盘对称位置镜像模仿你的上一手", "icon": "🪞"},
    "slip": {"name": "手滑了", "desc": "AI 有 14% 概率手滑到相邻的点位", "icon": "😾"},
    "blackhole": {"name": "黑洞", "desc": "棋盘中心 13 子区域对 AI 前 6 手禁入", "icon": "🕳️"},
    "exchange": {"name": "乾坤挪移", "desc": "强制 AI 虚手，你继续行棋（限 1 次）", "icon": "🔄", "uses": 1},
    "fog": {"name": "战争迷雾", "desc": "AI 前 11 手每手前会刷新一个 3×3 禁区遮罩；之后每回合随机封锁 2 个 AI 禁着点", "icon": "🌫️"},
    "gravity": {"name": "星位引力", "desc": "AI 前 7 手被星位磁场牵引", "icon": "🌃"},
    "golden_corner": {"name": "黄金角", "desc": "随机封锁一角 4×4 区域，AI 前 10 手禁入", "icon": "🪙"},
    "sansan": {"name": "三三开局", "desc": "强制 AI 在开局前 2 手去抢四个三三点中的位置，也就是开局硬走三三；之后 2 手暂时避开角上 4×4 区域", "icon": "◎"},
    "shadow": {"name": "影子", "desc": "AI 前 3 手有 70% 概率紧跟自己的上一手", "icon": "👁"},
    "sprout": {"name": "萌芽", "desc": "每次提子后，都会在附近自动长出 1 颗己棋", "icon": "🌱"},
    "joseki_ocd": {"name": "定式强迫症", "desc": "开局亮出 7 个目标点，只要下中 4 个，剩下的 3 个会自动补成你的棋子", "icon": "📻"},
    "handicap_quest": {"name": "让子任务", "desc": "先虚手 1 次，之后每满 8 手奖励 AI 虚手一次，最多触发 3 次", "icon": "🎵"},
    "god_hand": {"name": "神之一手", "desc": "踩中隐藏菱形区，周围 3×3 内随机爆出 3 颗己棋，只会落在空点", "icon": "✨"},
    "sansan_trap": {"name": "三三陷阱", "desc": "只有对手第 1 手正好下在四个三三点之一时才会触发，并在那手棋周围反生 8 颗我方棋", "icon": "🪤"},
    "corner_helper": {"name": "守角辅助", "desc": "每个角各算一次：任一角的 5×5 区域里有 4 颗己子时，就会在那个角补 1 颗援军", "icon": "🏯"},
    "sanrensei": {"name": "三连星", "desc": "若你前 2 手都落在星位，会自动补出第 3 颗星位棋，并再长出 2 颗援军", "icon": "⭐"},
    "no_regret": {"name": "永不悔棋", "desc": "禁用悔棋，但每手 12% 概率白送一子", "icon": "🚫"},
    "quickthink": {"name": "快速思考", "desc": "4 秒内落子可追加 2 秒连击窗口；选中后禁用推荐点位与悔棋", "icon": "⚡"},
    "foolish_wisdom": {"name": "大智若愚", "desc": "摆出愚形，附近 5×5 内随机长出 2 颗己棋", "icon": "🧠"},
    "five_in_row": {"name": "五子连珠", "desc": "这是五子棋，不是围棋。每当我方横、竖、斜正好连成 5 颗同色棋，就会优先在首尾补子；若首尾被堵住，则改在两端附近补子，并在连线附近再补 4 颗援军", "icon": "🎯"},
    "coach_mode": {"name": "代练上号", "desc": "主动技能：后 30 手由更强的 AI 代打；若下完后胜率仍低于 50%，则额外再代打 10 手", "icon": "🎗"},
    "capture_foul": {"name": "提子犯规", "desc": "若对手单次或累计提子达到 4 颗，就会触发“提子未放在棋盒”，被惩罚方罚 4 目，随后重新计数", "icon": "🧺"},
    "last_stand": {"name": "起死回生", "desc": "当我方胜率跌到 26% 以下时，仅触发 1 次：在上一手周围 3×3 内随机消掉 1 颗敌子，并随机补 1 颗己棋（不会落在禁着点）", "icon": "🫀"},
}

ROGUE_FEATURED_CARDS = {
    "god_hand",
    "sansan_trap",
    "corner_helper",
    "sanrensei",
    "no_regret",
    "quickthink",
    "foolish_wisdom",
    "five_in_row",
    "coach_mode",
    "capture_foul",
    "last_stand",
}

CHALLENGE_BETA_POOL = [
    "dice",
    "nerf",
    "time_press",
    "suboptimal",
    "seal",
    "blackhole",
    "golden_corner",
    "fog",
    "sprout",
    "joseki_ocd",
    "corner_helper",
    "sanrensei",
    "foolish_wisdom",
    "five_in_row",
    "sansan_trap",
    "god_hand",
    "twin",
    "exchange",
    "capture_foul",
    "last_stand",
]

CHALLENGE_BETA_HANDICAPS = {
    1: 0,
    2: 2,
}

CHALLENGE_CATEGORY_MAP = {
    "sanrensei": "derivative",
    "foolish_wisdom": "derivative",
    "five_in_row": "derivative",
    "sansan_trap": "trap",
    "god_hand": "trap",
    "blackhole": "zone",
    "golden_corner": "zone",
    "fog": "zone",
    "seal": "zone",
    "dice": "restriction",
    "nerf": "restriction",
    "time_press": "restriction",
    "suboptimal": "restriction",
    "twin": "active",
    "exchange": "active",
}

TWO_PLAYER_ROGUE_POOL = [
    "erosion",
    "sprout",
    "joseki_ocd",
    "god_hand",
    "sansan_trap",
    "corner_helper",
    "sanrensei",
    "foolish_wisdom",
    "five_in_row",
    "capture_foul",
]

AI_ROGUE_POOL = [
    "blackhole",
    "golden_corner",
    "fog",
    "sansan_trap",
]

ULTIMATE_CARDS = {
    "chain": {"name": "连珠棋", "desc": "每手 65% 概率触发追加行动", "icon": "🔥"},
    "proliferate": {"name": "无限增殖", "desc": "落子后 5×5 范围内爆出 5 颗同色棋", "icon": "🌸"},
    "double": {"name": "双刀流", "desc": "每回合固定连下 2 手，但整回合只计 1 手数", "icon": "⚔️"},
    "wildgrow": {"name": "狂野生长", "desc": "4 颗己子向四周蔓延扩张", "icon": "🌿"},
    "rejection": {"name": "排异反应", "desc": "落点 5×5 内敌子被推开或摧毁", "icon": "💥"},
    "territory": {"name": "绝对领地", "desc": "落点周围 4 格形成禁入结界", "icon": "🛡️"},
    "shadow_clone": {"name": "影分身", "desc": "先生成一颗镜像棋；下一回合会按原落点和镜像点强制连成一整条线，就算两端棋子被提掉也照样连线", "icon": "👥"},
    "plague": {"name": "瘟疫", "desc": "3×3 内所有敌子转化为己方", "icon": "☣️"},
    "meteor": {"name": "陨石雨", "desc": "随机轰掉 5 颗对方棋子", "icon": "☄️"},
    "quantum": {"name": "量子纠缠", "desc": "全盘随机位置生成 5 颗同色棋", "icon": "🌀"},
    "devour": {"name": "吞噬", "desc": "5×5 范围内敌子全部清空", "icon": "🦷"},
    "timewarp": {"name": "时空裂缝", "desc": "85% 概率抹去对手最近 2 手", "icon": "🕰️"},
    "blackout": {"name": "天崩地裂", "desc": "十字方向清除所有敌子", "icon": "🌋"},
    "magnet": {"name": "磁力吸附", "desc": "己方棋子飞速聚拢，碾碎路径上的敌子", "icon": "🧲"},
    "necro": {"name": "亡灵召唤", "desc": "召唤 3 颗己棋 + 策反 2 颗敌棋", "icon": "💀"},
    "wall": {"name": "万里长城", "desc": "有 60% 概率发动：整行或整列筑起一面不可逾越的棋墙", "icon": "🧱"},
    "joseki_burst": {"name": "定式爆发", "desc": "命中定式后补满目标，并额外爆出 50 颗同色棋", "icon": "📐"},
    "god_hand": {"name": "神之一手", "desc": "踩中 5×5 隐藏菱形，清空敌子并铺满 50 颗己棋", "icon": "✨"},
    "corner_helper": {"name": "守角要塞", "desc": "四个角分别独立结算：某个角的 5×5 区域里有 2 颗己子时，就会封满该角 8×8 边界并清掉里面的敌子", "icon": "🏯"},
    "sanrensei": {"name": "三连星爆发", "desc": "前 3 手全落星位，引爆全盘星位势力", "icon": "⭐"},
    "quickthink": {"name": "极速风暴", "desc": "5 秒内不限次数连续落子，结束后 AI 再读盘，整段只计 1 手数", "icon": "⚡"},
    "foolish_wisdom": {"name": "愚形连锁", "desc": "检测到愚形就连锁生成，最多铺满 20 颗己棋", "icon": "🧩"},
    "five_in_row": {"name": "五子连珠爆发", "desc": "这是五子棋，不是围棋。每当我方横、竖、斜正好连成 5 颗同色棋，就会随机清除对方 30 颗棋子，并在全盘随机补下 30 颗己棋；该效果可连锁触发", "icon": "🎯"},
    "capture_foul": {"name": "提子犯规", "desc": "若对手提子或技能消除棋子累计超过 5 颗，则 100% 触发“提子未放在棋盒”，被惩罚方立刻罚 50 目；每次触发后重新计数，之后仍可重复触发", "icon": "🧺"},
    "last_stand": {"name": "起死回生", "desc": "当我方胜率跌到 30% 以下时：全盘随机清除对方 30 颗棋子，并随机补下 30 颗己棋", "icon": "🫀"},
}

ULTIMATE_FEATURED_CARDS = {
    "joseki_burst",
    "god_hand",
    "corner_helper",
    "sanrensei",
    "quickthink",
    "foolish_wisdom",
    "five_in_row",
    "capture_foul",
    "last_stand",
}

AI_ULTIMATE_POOL = [
    "proliferate",
    "meteor",
    "quantum",
    "devour",
    "necro",
    "wall",
    "blackout",
    "wildgrow",
    "plague",
]

CARD_REQUIRED_FIELDS = ("name", "desc", "icon")
CHALLENGE_CATEGORIES = ("derivative", "trap", "zone", "restriction", "active")

ROGUE_CARD_META = {
    "puppet": {"tier": "S", "category": "主动", "complexity": "高"},
    "twin": {"tier": "A", "category": "主动", "complexity": "中"},
    "exchange": {"tier": "A", "category": "主动", "complexity": "低"},
    "coach_mode": {"tier": "S", "category": "主动", "complexity": "中"},
    "dice": {"tier": "B+", "category": "AI干扰", "complexity": "低"},
    "mirror": {"tier": "B+", "category": "AI干扰", "complexity": "低"},
    "slip": {"tier": "B+", "category": "AI干扰", "complexity": "低"},
    "god_hand": {"tier": "A", "category": "爆发", "complexity": "中"},
    "sansan_trap": {"tier": "A", "category": "陷阱", "complexity": "中"},
    "sanrensei": {"tier": "A", "category": "开局构筑", "complexity": "中"},
    "joseki_ocd": {"tier": "A", "category": "任务", "complexity": "中"},
    "no_regret": {"tier": "B+", "category": "风险收益", "complexity": "低"},
    "quickthink": {"tier": "A", "category": "节奏", "complexity": "高"},
    "five_in_row": {"tier": "A", "category": "连线构筑", "complexity": "高"},
}

ULTIMATE_CARD_META = {
    "chain": {"tier": "S", "category": "连动", "complexity": "低"},
    "double": {"tier": "S", "category": "连动", "complexity": "低"},
    "quickthink": {"tier": "S", "category": "节奏", "complexity": "高"},
    "joseki_burst": {"tier": "S", "category": "任务爆发", "complexity": "中"},
    "god_hand": {"tier": "S", "category": "爆发", "complexity": "中"},
    "five_in_row": {"tier": "S", "category": "连线构筑", "complexity": "高"},
}

DEFAULT_ROGUE_META = {"tier": "B", "category": "规则改写", "complexity": "中"}
DEFAULT_ULTIMATE_META = {"tier": "S", "category": "大招", "complexity": "中"}


def _missing_pool_entries(pool_name: str, pool: Iterable[str], catalog: dict[str, dict[str, Any]]) -> list[str]:
    return [f"{pool_name}:{card_id}" for card_id in pool if card_id not in catalog]


def validate_card_catalog() -> list[str]:
    """Return human-readable catalog errors for smoke tests and startup checks."""
    errors: list[str] = []
    for catalog_name, catalog in (("ROGUE_CARDS", ROGUE_CARDS), ("ULTIMATE_CARDS", ULTIMATE_CARDS)):
        for card_id, card in catalog.items():
            for field in CARD_REQUIRED_FIELDS:
                if not card.get(field):
                    errors.append(f"{catalog_name}.{card_id}: missing {field}")
            uses = card.get("uses")
            if uses is not None and (not isinstance(uses, int) or uses < 0):
                errors.append(f"{catalog_name}.{card_id}: invalid uses={uses!r}")

    for missing in _missing_pool_entries("ROGUE_FEATURED_CARDS", ROGUE_FEATURED_CARDS, ROGUE_CARDS):
        errors.append(f"unknown rogue featured card {missing}")
    for missing in _missing_pool_entries("CHALLENGE_BETA_POOL", CHALLENGE_BETA_POOL, ROGUE_CARDS):
        errors.append(f"unknown challenge card {missing}")
    for missing in _missing_pool_entries("TWO_PLAYER_ROGUE_POOL", TWO_PLAYER_ROGUE_POOL, ROGUE_CARDS):
        errors.append(f"unknown two-player rogue card {missing}")
    for missing in _missing_pool_entries("AI_ROGUE_POOL", AI_ROGUE_POOL, ROGUE_CARDS):
        errors.append(f"unknown AI rogue card {missing}")
    for missing in _missing_pool_entries("ULTIMATE_FEATURED_CARDS", ULTIMATE_FEATURED_CARDS, ULTIMATE_CARDS):
        errors.append(f"unknown ultimate featured card {missing}")
    for missing in _missing_pool_entries("AI_ULTIMATE_POOL", AI_ULTIMATE_POOL, ULTIMATE_CARDS):
        errors.append(f"unknown AI ultimate card {missing}")

    for card_id, category in CHALLENGE_CATEGORY_MAP.items():
        if card_id not in ROGUE_CARDS:
            errors.append(f"unknown challenge category card CHALLENGE_CATEGORY_MAP:{card_id}")
        if category not in CHALLENGE_CATEGORIES:
            errors.append(f"unknown challenge category {card_id}:{category}")
    return errors


def assert_valid_card_catalog() -> None:
    errors = validate_card_catalog()
    if errors:
        raise ValueError("Invalid card catalog:\n" + "\n".join(errors))


def get_rogue_card(card_id: str) -> dict[str, Any]:
    return ROGUE_CARDS[card_id]


def get_ultimate_card(card_id: str) -> dict[str, Any]:
    return ULTIMATE_CARDS[card_id]


def rogue_card_meta(card_id: str) -> dict[str, str]:
    return {**DEFAULT_ROGUE_META, **ROGUE_CARD_META.get(card_id, {})}


def ultimate_card_meta(card_id: str) -> dict[str, str]:
    return {**DEFAULT_ULTIMATE_META, **ULTIMATE_CARD_META.get(card_id, {})}


def rogue_card_summary(card_id: str) -> dict[str, Any]:
    card = get_rogue_card(card_id)
    return {"id": card_id, "name": card["name"], "desc": card["desc"], "icon": card["icon"], "meta": rogue_card_meta(card_id)}


def ultimate_card_summary(card_id: str) -> dict[str, Any]:
    card = get_ultimate_card(card_id)
    return {"id": card_id, "name": card["name"], "desc": card["desc"], "icon": card["icon"], "meta": ultimate_card_meta(card_id)}


def rogue_card_ids(pool: Iterable[str] | None = None, exclude: Iterable[str] | None = None) -> list[str]:
    excluded = set(exclude or [])
    source = list(pool) if pool is not None else list(ROGUE_CARDS.keys())
    return [card_id for card_id in source if card_id in ROGUE_CARDS and card_id not in excluded]


def ultimate_card_ids(exclude: Iterable[str] | None = None) -> list[str]:
    excluded = set(exclude or [])
    return [card_id for card_id in ULTIMATE_CARDS if card_id not in excluded]


def featured_rogue_cards(pool: Iterable[str] | None = None) -> list[str]:
    source = rogue_card_ids(pool)
    return [card_id for card_id in source if card_id in ROGUE_FEATURED_CARDS]


def featured_ultimate_cards(pool: Iterable[str] | None = None) -> list[str]:
    source = list(pool) if pool is not None else list(ULTIMATE_CARDS.keys())
    return [card_id for card_id in source if card_id in ULTIMATE_FEATURED_CARDS]


def challenge_card_category(card_id: str) -> str | None:
    return CHALLENGE_CATEGORY_MAP.get(card_id)


def challenge_category_counts(cards: Iterable[str]) -> dict[str, int]:
    counts = {category: 0 for category in CHALLENGE_CATEGORIES}
    for card_id in cards:
        category = challenge_card_category(card_id)
        if category:
            counts[category] += 1
    return counts


def ai_rogue_cards(exclude: Iterable[str] | None = None) -> list[str]:
    return rogue_card_ids(AI_ROGUE_POOL, exclude=exclude)


def ai_ultimate_cards(exclude: Iterable[str] | None = None) -> list[str]:
    excluded = set(exclude or [])
    return [card_id for card_id in AI_ULTIMATE_POOL if card_id in ULTIMATE_CARDS and card_id not in excluded]


assert_valid_card_catalog()
