from .monster import FireMonster, WaterMonster, GrassMonster
from .monster.move import Attack, Defend, Rampage, Poison, DrainEnergy
from .game_manager import FightManager


if __name__ == "__main__":
    attack = Attack()
    rampage = Rampage()
    defend = Defend()
    poison = Poison()
    drain_energy = DrainEnergy()

    num_players = input("How many players? 1/2: ")
    ai_p2 = False

    if num_players == "1":
        ai_p2 = True


    nick = input("Player 1: Choose your monster's name: ")

    monster_1 = GrassMonster(
        health=5,
        energy=5,
        moves=[
            attack,
            rampage,
            defend,
            poison,
            drain_energy,
        ],
        nickname=nick
    )

    nick = "Computer"
    if not ai_p2:
        nick = input("Player 2: Choose your monster's name: ")

    monster_2 = GrassMonster(
        health=5,
        energy=5,
        moves=[
            attack,
            rampage,
            defend,
            poison,
            drain_energy,
        ],
        nickname=nick
    )

    fight_manager = FightManager(monster_1, monster_2, ai_p2)
    fight_manager.loop()
