import random
from .characters import Player, Dragon


def attack(attacker, defender):
    if isinstance(attacker, Player):
        if attacker.role == "Knight" and attacker.charged:
            dmg = int(random.randint(attacker.min_dmg + 4, attacker.max_dmg + 6) * 1.75)
            crit = random.random() < attacker.total_crit()
            if crit:
                dmg = int(dmg * 1.6)
            if random.random() >= defender.total_dodge():
                defender.hp -= dmg
                print(f"Мощный удар! Урон: {dmg}{' КРИТ' if crit else ''}\n")
            else:
                print("Дракон увернулся!\n")
            attacker.charged = False
            return
        elif attacker.role == "Knight":
            from .utils import prompt

            choice = prompt("Выберите:", {"1": "Быстрый удар", "2": "Мощный заряд (2 хода)"})
            if choice == "2":
                attacker.charged = True
                print("Заряд! Следующий ход - мощный удар.\n")
                return
            dmg = random.randint(attacker.min_dmg, attacker.max_dmg)
        elif attacker.role == "Archer":
            from .utils import prompt

            choice = prompt("Выберите:", {"1": "Стрела", "2": "Тяжёлая стрела (+шанс промаха)"})
            if choice == "2" and random.random() < 0.3:
                print("Тяжёлая стрела пролетела мимо!\n")
                return
            dmg = random.randint(attacker.min_dmg, attacker.max_dmg)
            if choice == "2":
                dmg = random.randint(attacker.min_dmg + 3, attacker.max_dmg + 5)
        else:
            from .utils import prompt

            choice = prompt("Выберите:", {"1": "Заклинание", "2": "Гром(+шанс стана)"})
            if choice == "2":
                dmg = random.randint(attacker.min_dmg + 3, attacker.max_dmg + 6)
                stun = random.random() < 0.35
            else:
                dmg = random.randint(attacker.min_dmg, attacker.max_dmg + 2)
                stun = False
            crit = random.random() < attacker.total_crit()
            if crit:
                dmg = int(dmg * 1.6)
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
        if crit:
            dmg = int(dmg * 1.6)
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
        if breath:
            dmg = int(dmg * 1.2)
        crit = random.random() < attacker.crit_chance
        if crit:
            dmg = int(dmg * 1.5)
        if random.random() >= defender.total_dodge():
            defender.hp -= dmg
            print(f"Дракон {'изрыгает пламя' if breath else 'наносит удар'} на {dmg}!\n")
        else:
            print("Вы увернулись!\n")


