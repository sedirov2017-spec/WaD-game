import random

from .characters import Player
from .combat import attack
from .factory import create_dragon
from .utils import prompt, show_status


def main():
    random.seed()
    print("=== Битва с Драконом ===")
    diff_mod = {
        "player_hp": 100,
        "dragon_hp": 120,
        "heal": 3,
        "crit": 2,
        "dodge": 2,
        "crit_bonus": 0,
        "dodge_bonus": 0,
        "dragon_mult": 1.0,
    }

    role_choice = prompt("Выберите класс:", {"1": "Рыцарь", "2": "Лучник", "3": "Маг"})
    roles_map = {"1": "Knight", "2": "Archer", "3": "Mage"}
    role = roles_map[role_choice]

    if role == "Knight":
        base = (10, 16, 0.10, 0.08)
    elif role == "Archer":
        base = (8, 14, 0.14, 0.12)
    else:
        base = (9, 13, 0.12, 0.10)

    player = Player(role, diff_mod["player_hp"], base[0], base[1], base[2], base[3])
    dragon = create_dragon(diff_mod)

    print(f"\nВы {role}. Битва началась!\n")
    can_attempt_tame = True

    while player.hp > 0 and dragon.hp > 0:
        show_status(player, dragon)
        player.apply_buffs()

        act = prompt("Ваш ход:", {"1": "Атаковать", "2": "Выпить зелье"})
        if act == "2":
            p_choice = prompt("Выберите зелье:", {"1": "Лечение", "2": "Крит", "3": "Уворот"})
            if p_choice == "1":
                player.use_potion("heal")
            elif p_choice == "2":
                player.use_potion("crit")
            else:
                player.use_potion("dodge")
        else:
            attack(player, dragon)

        if dragon.hp < 20 and can_attempt_tame:
            choice = prompt("Вы хотите приручить дракона?", {"1": "Да", "2": "Нет"})
            if choice == "1":
                print("Вы приручили дракона! Победа!\n")
                break
            elif choice == "2":
                can_attempt_tame = False

        if dragon.hp <= 0:
            print("Вы победили дракона!\n")
            break

        attack(dragon, player)
        if player.hp <= 0:
            print("К сожалению, вы потерпели поражение...\n")
            break

    print("Конец.")
    try:
        input("Нажмите Enter для выхода...")
    except EOFError:
        pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nВыход.")


