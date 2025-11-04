import random


class Character:
    def __init__(self, max_hp, min_dmg, max_dmg, crit_chance, dodge_chance):
        self.hp = self.max_hp = max_hp
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
        self.crit_chance = crit_chance
        self.dodge_chance = dodge_chance
        self.buffs = {"crit": 0, "dodge": 0}
        self.buffs_time = {"crit": 0, "dodge": 0}

    def apply_buffs(self):
        for buff in list(self.buffs):
            if self.buffs_time[buff] > 0:
                self.buffs_time[buff] -= 1
                if self.buffs_time[buff] == 0:
                    self.buffs[buff] = 0

    def total_crit(self):
        return min(1, self.crit_chance + self.buffs["crit"])

    def total_dodge(self):
        return min(1, self.dodge_chance + self.buffs["dodge"])


class Player(Character):
    def __init__(self, role, hp, min_d, max_d, crit, dodge):
        super().__init__(hp, min_d, max_d, crit, dodge)
        self.role = role
        self.potions = {"heal": 5, "crit": 3, "dodge": 3}
        self.charged = False

    def use_potion(self, p_type):
        if self.potions[p_type] <= 0:
            print("Зелий нет!\n")
            return
        self.potions[p_type] -= 1
        if p_type == "heal":
            heal_amount = max(18, int(self.max_hp * 0.35))
            self.hp = min(self.max_hp, self.hp + heal_amount)
            print(f"Восстановлено {heal_amount} HP.\n")
        else:
            self.buffs[p_type] = 0.20
            self.buffs_time[p_type] = 3
            print(f"Усиление {p_type} на 3 хода!\n")


class Dragon(Character):
    def __init__(self, hp, min_d, max_d, crit, dodge):
        super().__init__(hp, min_d, max_d, crit, dodge)
        self.stunned = False


