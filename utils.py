def prompt(msg, options):
    while True:
        print(msg)
        for k, v in options.items():
            print(f"{k} {v}")
        c = input("> ").strip()
        if c in options:
            return c
        print("Некорректный выбор.\n")


def show_status(player, dragon):
    print("=" * 50)
    print(f"Ваш HP: {player.hp}/{player.max_hp}")
    print(f"Дракон HP: {dragon.hp}/{dragon.max_hp}")
    print(f"Крит: {int(player.total_crit()*100)}% Уворот: {int(player.total_dodge()*100)}%")
    print(
        f"Зелья: Леч: {player.potions['heal']} Crit: {player.potions['crit']} Уворот: {player.potions['dodge']}"
    )
    print("=" * 50)


