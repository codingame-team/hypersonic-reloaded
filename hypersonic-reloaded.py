from collections import deque

from random import choice

from numpy import array, zeros
from typing import List, Optional

from dataclasses import dataclass

import sys
import math


def idebug(*args):
    return
    print(*args, file=sys.stderr)


def debug(*args):
    # return
    print(*args, file=sys.stderr)


@dataclass
class Position:
    x: int
    y: int

    def dist(self, other) -> int:
        return abs(other.x - self.x) + abs(other.y - self.y)

    def __eq__(self, other) -> int:
        return other.x == self.x and other.y == self.y

    def __repr__(self):
        return f'{self.x} {self.y}'


@dataclass
class Player:
    id: int
    pos: Position
    bombs: int  # le nombre de bombes qu'il peut encore placer
    b_range: int  # la valeur de portée des bombes de ce joueur
    target: Optional[Position]


@dataclass
class Bomb:
    owner: int
    pos: Position
    countdown: int  # le nombre de tours de jeu restants avant que la bombe explose.
    range: int  # la valeur de portée de cette bombe


def bomb_damage(player: Player, pos: Position) -> int:
    """
        Calculate number of boxes' explosions
    :param player: player launching the bomb
    :param pos: position of the bomb
    :return: damage score of bomb
    """
    damage: int = 0
    x, y = pos.x, pos.y
    for _ in range(1, player.b_range):
        x += 1
        if not 0 <= x < width:
            break
        elif boxes[x, y] == 1:
            damage += 1
            break
    x, y = pos.x, pos.y
    for _ in range(1, player.b_range):
        x -= 1
        if not 0 <= x < width:
            break
        elif boxes[x, y] == 1:
            damage += 1
            break
    x, y = pos.x, pos.y
    for _ in range(1, player.b_range):
        y += 1
        if not 0 <= y < height:
            break
        elif boxes[x, y] == 1:
            damage += 1
            break
    x, y = pos.x, pos.y
    for _ in range(1, player.b_range):
        y -= 1
        if not 0 <= y < height:
            break
        elif boxes[x, y] == 1:
            damage += 1
            break
    return damage


def safe_path(pos: Position) -> bool:
    pass


def get_player(player_id: int) -> Optional[Player]:
    player_list = [p for p in players if p.id == player_id]
    return player_list[0] if player_list else None


in_grid = lambda x, y: 0 <= x < width and 0 <= y < height

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
PLAYER = 0
BOMB = 1
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

width, height, my_id = [int(i) for i in input().split()]
idebug(width, height, my_id)

players: List[Player] = []

# game loop
while True:
    boxes: array = zeros(shape=(width, height), dtype=int)
    t_boxes = boxes.T
    bombs: List[Bomb] = []
    for i in range(height):
        row = input()
        idebug(row)
        for j, value in enumerate(list(row)):
            boxes[j, i] = 1 if value == '0' else 0
    entities = int(input())
    idebug(entities)
    for i in range(entities):
        entity_type, owner, x, y, param_1, param_2 = [int(j) for j in input().split()]
        idebug(entity_type, owner, x, y, param_1, param_2)
        pos: Position = Position(x, y)
        if entity_type == PLAYER:
            player: Player = get_player(player_id=owner)
            if player:
                player.pos, player.bombs = pos, param_1
            else:
                players.append(Player(id=owner, pos=pos, bombs=param_1, b_range=param_2, target=None))
        else:
            bombs.append(Bomb(owner=owner, pos=pos, countdown=param_1, range=param_2))

    player: Player = [p for p in players if p.id == my_id][0]
    opponent: Player = [p for p in players if p.id != my_id][0]

    my_bombs: List[Bomb] = [b for b in bombs if b.owner == my_id]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    available_moves: List[Position] = [Position(x, y) for x in range(width) for y in range(height) if not boxes[x, y]]

    if player.target:
        debug(f'player bringing bomb to {player.target}')

    if player.bombs:
        if player.target:
            if player.pos == player.target:
                print(f'BOMB {player.pos} BOMB {player.pos}')
                available_moves.remove(player.target)
                player.target = None
            else:
                print(f'MOVE {player.target}')
        else:
            # bomb_candidates = [(p, bomb_damage(player, p)) for p in available_moves]
            # bomb_candidates.sort(key=lambda x: x[1], reverse=True)
            player.target = max(available_moves, key=lambda p: bomb_damage(player, p) / (1 + p.dist(player.pos)))
            #player.target = max(available_moves, key=lambda p: bomb_damage(player, p))
            print(f'MOVE {player.target}')
    else:
        if my_bombs:
            best_move: Position = max(available_moves, key=lambda p: sum([p.dist(b.pos) for b in bombs]))
            print(f'MOVE {best_move}')
        else:
            move: Position = choice(available_moves)
            print(f'MOVE {move}')
