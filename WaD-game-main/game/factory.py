from .characters import Player, Dragon


def create_character(role, diff_mod):
    roles = {
        "Knight": (10, 16, 0.10, 0.08),
        "Archer": (8, 14, 0.14, 0.12),
        "Mage": (9, 13, 0.12, 0.10),
    }
    min_d, max_d, crit, dodge = roles[role]
    max_hp = diff_mod["player_hp"]
    return Player(
        role,
        max_hp,
        min_d,
        max_d,
        crit + diff_mod["crit_bonus"],
        dodge + diff_mod["dodge_bonus"],
    )


def create_dragon(diff_mod):
    min_d, max_d = 9, 15
    crit, dodge = 0.10, 0.06
    hp = diff_mod["dragon_hp"]
    mult = diff_mod["dragon_mult"]
    return Dragon(hp, int(min_d * mult), int(max_d * mult), crit, dodge)


