import os
import random
from time import sleep

from .monster.exceptions import OutOfEnergyException


def clear_screen():
    os.system("cls||clear")


class FightManager:
    def __init__(self, m1, m2, ai_p2=True):
        self.m1 = m1
        self.m2 = m2
        self.ai_p2 = ai_p2
        self.last_move = None

    def print_monsters(self, player):
        if player == self.m1:
            m1 = self.m1
            m2 = self.m2
        else:
            m1 = self.m2
            m2 = self.m1
        print(
            f"Your monster: {m1.name}\nHealth: {round(m1.health, 2)}\n"
            f"Energy: {m1.energy}\nState: {m1.state}\n"
        )
        print(
            f"Their monster: {m2.name}\nHealth: {round(m2.health, 2)}\n"
            f"Energy: {m2.energy}\nState: {m2.state}\n"
        )

    def check_win(self):
        if self.m1.health <= 0:
            print("PLAYER 2 WINS!!!")
            return True
        if self.m2.health <= 0:
            print("PLAYER 1 WINS!!!")
            return True
        return False

    def player_go(self, player_mon, enemy_mon):
        if self.last_move:
            print(self.last_move)
        self.print_monsters(player_mon)
        player_mon.list_moves()
        while True:
            try:
                choice = int(input("Select your move! \n"))
                if choice > len(player_mon.moves):
                    raise RuntimeError
            except (RuntimeError, TypeError):
                print("Choose a valid number!\n")
            else:
                print()
                try:
                    player_mon.perform_move(choice, enemy_mon)
                    clear_screen()
                    message = f"{player_mon.name} used {player_mon.moves[choice - 1].name}!\n"
                    self.last_move = message
                    break
                except OutOfEnergyException:
                    print("Out of energy!  Choose a different move\n")


    def ai_go(self, ai_mon, player_mon):
        while True:
            choice = random.randint(1, len(ai_mon.moves))
            try:
                ai_mon.perform_move(choice, player_mon)
                message = f"{ai_mon.name} used {ai_mon.moves[choice - 1].name}!\n"
                print(message)
                self.last_move = message
                break
            except OutOfEnergyException:
                pass
        sleep(1.7)
        clear_screen()

    def turn(self, first, second):
        first()
        if self.check_win():
            return True
        second()
        if self.check_win():
            return True
        return False

    def loop(self):
        clear_screen()

        first_player = random.choice((self.m1, self.m2))
        player_one_turn = lambda: self.player_go(self.m1, self.m2)

        if self.ai_p2:
            player_two_turn = lambda: self.ai_go(self.m2, self.m1)
        else:
            player_two_turn = lambda: self.player_go(self.m2, self.m1)

        if first_player == self.m1:
            next_turn = lambda: self.turn(player_one_turn, player_two_turn)
        else:
            next_turn = lambda: self.turn(player_one_turn, player_two_turn)

        while True:
            if next_turn():
                break
