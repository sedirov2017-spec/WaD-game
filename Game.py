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
    def total_crit(self): return min(1, self.crit_chance + self.buffs["crit"])
    def total_dodge(self): return min(1, self.dodge_chance + self.buffs["dodge"])

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

def prompt(msg, options):
    while True:
        print(msg)
        for k, v in options.items():
            print(f"{k}) {v}")
        c = input("> ").strip()
        if c in options:
            return c
        print("Некорректный выбор.\n")

def create_character(role, diff_mod):
    roles = {
        "Knight": (10, 16, 0.10, 0.08),
        "Archer": (8, 14, 0.14, 0.12),
        "Mage": (9, 13, 0.12, 0.10),
    }
    min_d, max_d, crit, dodge = roles[role]
    max_hp = diff_mod["player_hp"]
    return Player(role, max_hp, min_d, max_d, crit + diff_mod["crit_bonus"], dodge + diff_mod["dodge_bonus"])

def create_dragon(diff_mod):
    min_d, max_d = 9, 15
    crit, dodge = 0.10, 0.06
    hp = diff_mod["dragon_hp"]
    mult = diff_mod["dragon_mult"]
    return Dragon(hp, int(min_d*mult), int(max_d*mult), crit, dodge)

def attack(attacker, defender):
    if isinstance(attacker, Player):
        if attacker.role == "Knight" and attacker.charged:
            dmg = int(random.randint(attacker.min_dmg+4, attacker.max_dmg+6) * 1.75)
            crit = random.random() < attacker.total_crit()
            if crit: dmg = int(dmg * 1.6)
            if random.random() >= defender.total_dodge():
                defender.hp -= dmg
                print(f"Мощный удар! Урон: {dmg}{' КРИТ' if crit else ''}\n")
            else:
                print("Дракон увернулся!\n")
            attacker.charged = False
            return
        elif attacker.role == "Knight":
            choice = prompt("Выберите:", {"1": "Быстрый удар", "2": "Мощный заряд"})
            if choice == "2":
                attacker.charged = True
                print("Заряд! Следующий ход - мощный удар.\n")
                return
            dmg = random.randint(attacker.min_dmg, attacker.max_dmg)
        elif attacker.role == "Archer":
            choice = prompt("Выберите:", {"1": "Стрела", "2": "Тяжёлая стрела"})
            if choice == "2" and random.random() < 0.3:
                print("Тяжёлая стрела пролетела мимо!\n")
                return
            dmg = random.randint(attacker.min_dmg, attacker.max_dmg)
            if choice == "2": dmg = random.randint(attacker.min_dmg+3, attacker.max_dmg+5)
        else:
            choice = prompt("Выберите:", {"1": "Заклинание", "2": "Гром"})
            if choice == "2":
                dmg = random.randint(attacker.min_dmg+3, attacker.max_dmg+6)
                stun = random.random() < 0.35
            else:
                dmg = random.randint(attacker.min_dmg, attacker.max_dmg+2)
                stun = False
            crit = random.random() < attacker.total_crit()
            if crit: dmg = int(dmg * 1.6)
            if random.random() >= defender.total_dodge():
                defender.hp -= dmg
                print(f"Магия! Урон: {dmg}{' КРИТ' if crit else ''}")
                if choice == "2" and stun and defender.hp > 0:
                    defender.stunned = True
                    print("Дракон оглушён!\n")
            else:
                print("Дракон увернулся!\n")
            return
        crit = random.random() < attacker.total_crit()
        if crit: dmg = int(dmg * 1.6)
        if random.random() >= defender.total_dodge():
            defender.hp -= dmg
            print(f"Удар! Урон: {dmg}{' КРИТ' if crit else ''}\n")
        else:
            print("Дракон увернулся!\n")
    elif isinstance(attacker, Dragon):
        if attacker.stunned:
            print("Дракон оглушён и пропускает ход!\n")
            attacker.stunned = False
            return
        breath = random.random() < 0.2
        dmg = random.randint(attacker.min_dmg, attacker.max_dmg)
        if breath: dmg = int(dmg * 1.2)
        crit = random.random() < attacker.crit_chance
        if crit: dmg = int(dmg * 1.5)
        if random.random() >= defender.total_dodge():
            defender.hp -= dmg
            print(f"Дракон {'изрыгает пламя' if breath else 'наносит удар'} на {dmg}!\n")
        else:
            print("Вы увернулись!\n")

def show_status(player, dragon):
    print("="*50)
    print(f"Ваш HP: {player.hp}/{player.max_hp}")
    print(f"Дракон HP: {dragon.hp}/{dragon.max_hp}")
    print(f"Крит: {int(player.total_crit()*100)}% Уворот: {int(player.total_dodge()*100)}%")
    print(f"Зелья: Леч: {player.potions['heal']} Crit: {player.potions['crit']} Уворот: {player.potions['dodge']}")
    print("="*50)

def main():
    random.seed()
    print("=== Битва с Драконом ===")
    # Настройка сложности
    diff_mod = {
        "player_hp": 100, "dragon_hp": 120,
        "heal": 3, "crit": 2, "dodge": 2,
        "crit_bonus": 0, "dodge_bonus": 0,
        "dragon_mult": 1.0
    }
    role_choice = prompt("Выберите класс:", {"1": "Рыцарь", "2": "Лучник", "3": "Маг"})
    roles_map = {"1": "Knight", "2": "Archer", "3": "Mage"}
    role = roles_map[role_choice]
    if role == "Knight": base = (10, 16, 0.10, 0.08)
    elif role == "Archer": base = (8, 14, 0.14, 0.12)
    else: base = (9, 13, 0.12, 0.10)
    player = Player(role, diff_mod["player_hp"], base[0], base[1], base[2], base[3])
    dragon = create_dragon(diff_mod)
    print(f"\nВы {role}. Битва началась!\n")
    while player.hp > 0 and dragon.hp > 0:
        show_status(player, dragon)
        player.apply_buffs()
        act = prompt("Ваш ход:", {"1": "Атаковать", "2": "Выпить зелье"})
        if act == "2":
            p_choice = prompt("Выберите зелье:", {"1": "Лечение", "2": "Крит", "3": "Уворот"})
            if p_choice == "1": player.use_potion("heal")
            elif p_choice == "2": player.use_potion("crit")
            else: player.use_potion("dodge")
        else:
            attack(player, dragon)
        flag = 1
        if dragon.hp < 20 and flag == 1:
            choice = prompt("Вы хотите приручить дракона?", {"1": "Нет", "2": "Да"})
            if choice == "2":
                print("Вы приручили дракона! Победа!\n")
                break
            else:
                flag = 0

        if dragon.hp <= 0:
            print("Вы победили дракона!\n")
            break
        attack(dragon, player)
        if player.hp <= 0:
            print("К сожалению, вы потерпели поражение...\n")
            break
    print("Конец.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nВыход.")