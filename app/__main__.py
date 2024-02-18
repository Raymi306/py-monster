import random

from .monster import FireMonster, WaterMonster
from .monster import Attack, Defend, Rampage, Poison, DrainEnergy
from .monster import OutOfEnergyException

attack = Attack()
rampage = Rampage()
defend = Defend()
poison = Poison()
drain_energy = DrainEnergy()

m1 = FireMonster(5, 5, [attack, rampage, poison])
m2 = WaterMonster(5, 5, [attack, defend, drain_energy])


def player_go(m1, m2):
    m1.list_moves()
    while True:
        try:
            choice = int(input("Select your move! \n"))
            if choice > len(m1.moves):
                raise RuntimeError
        except (RuntimeError, TypeError):
            print("Choose a valid number!\n")
        else:
            print()
            try:
                m1.perform_move(choice, m2)
                break
            except OutOfEnergyException:
                print("Out of energy!  Choose a different move\n")


def ai_go(m2, m1):
    while True:
        choice = random.randint(1, len(m2.moves))
        try:
            m2.perform_move(choice, m1)
            print(f"{m2.name} uses {m2.moves[choice - 1].name}!\n")
            break
        except OutOfEnergyException:
            pass


def game_loop():
    while True:
        print("TURN START!\n")
        print(f"Your monster: {m1.name}\nHealth: {round(m1.health, 2)}\nEnergy: {m1.energy}\nState: {m1.state}\n")
        print(f"Their monster: {m2.name}\nHealth: {round(m2.health, 2)}\nEnergy: {m2.energy}\nState: {m2.state}\n")

        who_goes = random.choice((m1, m2))

        if who_goes is m1:
            player_go(m1, m2)
            ai_go(m2, m1)
        else:
            ai_go(m2, m1)
            player_go(m1, m2)

        if m1.health <= 0:
            print("PLAYER 2 WINS!!!")
            break
        if m2.health <= 0:
            print("PLAYER 1 WINS!!!")
            break


if __name__ == "__main__":
    game_loop()
