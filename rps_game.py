#!/usr/bin/env python

from __future__ import annotations
from enum import Enum
import random

class Weapon(Enum):
    ROCK = "🪨"
    PAPER = "🧻"
    SCISSOR = "✂️"
    LIZARD = "🦎"
    SPOCK = "🖖"

    @classmethod
    def win_map(cls) -> dict[Weapon, list[Weapon]]:
        return {
            cls.ROCK: [cls.LIZARD, cls.SCISSOR],
            cls.PAPER: [cls.ROCK, cls.SPOCK],
            cls.SCISSOR: [cls.PAPER, cls.LIZARD],
            cls.LIZARD: [cls.SPOCK, cls.PAPER],
            cls.SPOCK: [cls.ROCK, cls.SCISSOR]
        }

    def wins_against(self, other: Weapon) -> bool:
        return other in Weapon.win_map()[self]

    def __str__(self) -> str:
        return self._value_

class PlayerInterface(object):
    def __init__(self, name: str) -> None:
        self.name = name

    def pick_weapon(self, choices: list[Weapon]) -> Weapon:
        pass # To be implemented.

    def __str__(self):
        return self.name

class RandomPlayer(PlayerInterface):
    """ Picks a random weapon every time. """
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def pick_weapon(self, choices: list[Weapon]) -> Weapon:
        return random.choice(choices)

class RockPlayer(PlayerInterface):
    """ Always picks rock if it's part of the game, otherwise picks randomly """
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def pick_weapon(self, choices: list[Weapon]) -> Weapon:
        if Weapon.ROCK in choices:
            return Weapon.ROCK
        else:
            return random.choice(choices)

class PsychPlayer(PlayerInterface):
    """ Prefers the weapon that it's initialized with, but will pick a random weapon every 3rd game. """
    def __init__(self, name: str, preferred_weapon: Weapon) -> None:
        super().__init__(name)
        self.preferred_weapon = preferred_weapon
        self.num_picks = 0

    def pick_weapon(self, choices: list[Weapon]) -> Weapon:
        self.num_picks += 1
        if self.preferred_weapon in choices and self.num_picks % 3 != 0:
            return self.preferred_weapon
        else:
            return random.choice(choices)


class RpsGame(object):
    def __init__(self, allowed_weapons: list[Weapon]) -> None:
        self.allowed_weapons = allowed_weapons

    # Returns a tuple where the first part is the list of winners, and the second part
    # is a map of everyone's choices for that game.
    def play_round(self, players: list[PlayerInterface]) -> tuple[list[PlayerInterface], dict[PlayerInterface, Weapon]]:
        """ Could be multiple winners (a tie) or zero winners (self destruction) """
        choices = {}
        for p in players:
            choices[p] = p.pick_weapon(self.allowed_weapons[:])

        left_standing = set(players)
        weapons_played = choices.values()
        for p, weapon_chosen in choices.items():
            for other_weapon in weapons_played:
                if other_weapon.wins_against(weapon_chosen):
                    left_standing.discard(p)

        return list(left_standing), choices

if __name__ == "__main__":
    manoj = RockPlayer("Manoj")
    james = PsychPlayer("James", Weapon.SCISSOR)
    bai = RandomPlayer("Sheng Bai")

    game = RpsGame([Weapon.ROCK, Weapon.SCISSOR, Weapon.PAPER])
    for i in range(10):
        print("Starting game: ", i + 1)
        winners, choices = game.play_round([manoj, james, bai])
        for p, w in choices.items():
            print("\t", p, "played", w)
        print()
        if len(winners) == 0:
            print("\tThere were no winners this round!")
        elif len(winners) == 1:
            print("\tRound champion was", winners[0])
        else:
            print("\tThe game was a tie with ", end="")
            print(*winners, sep=", ")
        print()
