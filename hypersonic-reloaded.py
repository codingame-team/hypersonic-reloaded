from __future__ import annotations

from collections import deque
from time import perf_counter

from enum import Enum

from copy import copy

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


"""
    Extra Portée : les bombes du joueur explosent avec une portée accrue de une unité. 
                    Cela ne s'applique pas aux bombes déjà en jeu.
    Extra Bombe : le joueur peut avoir une bombe de plus en jeu à la fois.
"""


class ItemType(Enum):
    XTRA_RANGE = 1
    XTRA_BOMB = 2


@dataclass
class Position:
    x: int
    y: int

    def dist(self, other) -> int:
        return abs(other.x - self.x) + abs(other.y - self.y)

    def is_bomb(self, bombs: List[Bomb]) -> int:
        return any([self == b.pos for b in bombs])

    def __eq__(self, other) -> int:
        return other.x == self.x and other.y == self.y

    def __copy__(self):
        return Position(self.x, self.y)

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

    def __eq__(self, other):
        return self.pos == other.pos

    def __copy__(self):
        return Bomb(self.owner, copy(self.pos), self.countdown, self.range)


@dataclass
class Item:
    type: ItemType
    pos: Position


def bomb_damage(player: Player, pos: Position, bombs: List[Bomb]) -> int:
    """
        Calculate number of boxes' explosions
    :param player: player launching the bomb
    :param pos: position of the bomb
    :return: damage score of bomb
    """
    active_bombs: List[Bomb] = [copy(b) for b in bombs]
    if pos.is_bomb(bombs):
        bomb: Bomb = [b for b in active_bombs if b.pos == pos][0]
        active_bombs.remove(bomb)
    damage: int = 0
    x, y = pos.x, pos.y
    for _ in range(1, player.b_range):
        x += 1
        if not 0 <= x < width:
            break
        elif walls[x, y]:
            break
        elif boxes[x, y] != -1:
            damage += boxes[x, y] + 1
            break
        else:
            new_pos = Position(x, y)
            if new_pos.is_bomb(active_bombs):
                damage += bomb_damage(player, new_pos, active_bombs)
                break
    x, y = pos.x, pos.y
    for _ in range(1, player.b_range):
        x -= 1
        if not 0 <= x < width:
            break
        elif walls[x, y]:
            break
        elif boxes[x, y] != -1:
            damage += boxes[x, y] + 1
            break
        else:
            new_pos = Position(x, y)
            if new_pos.is_bomb(active_bombs):
                damage += bomb_damage(player, new_pos, active_bombs)
                break
    x, y = pos.x, pos.y
    for _ in range(1, player.b_range):
        y += 1
        if not 0 <= y < height:
            break
        elif walls[x, y]:
            break
        elif boxes[x, y] != -1:
            damage += boxes[x, y] + 1
            break
        else:
            new_pos = Position(x, y)
            if new_pos.is_bomb(active_bombs):
                damage += bomb_damage(player, new_pos, active_bombs)
                break
    x, y = pos.x, pos.y
    for _ in range(1, player.b_range):
        y -= 1
        if not 0 <= y < height:
            break
        elif walls[x, y]:
            break
        elif boxes[x, y] != -1:
            damage += boxes[x, y] + 1
            break
        else:
            new_pos = Position(x, y)
            if new_pos.is_bomb(active_bombs):
                damage += bomb_damage(player, new_pos, active_bombs)
                break
    return damage

def bomb_kills(pos: Position, bomb: Bomb) -> bool:
    x, y = bomb.pos.x, bomb.pos.y
    for _ in range(1, opponent.b_range):
        x += 1
        if not 0 <= x < width or walls[x, y] or boxes[x, y] != -1:
            break
        elif (x, y) == (pos.x, pos.y):
            return True
    x, y = bomb.pos.x, bomb.pos.y
    for _ in range(1, opponent.b_range):
        x -= 1
        if not 0 <= x < width or walls[x, y] or boxes[x, y] != -1:
            break
        elif (x, y) == (pos.x, pos.y):
            return True
    x, y = bomb.pos.x, bomb.pos.y
    for _ in range(1, opponent.b_range):
        y += 1
        if not 0 <= y < height or walls[x, y] or boxes[x, y] != -1:
            break
        elif (x, y) == (pos.x, pos.y):
            return True
    x, y = bomb.pos.x, bomb.pos.y
    for _ in range(1, opponent.b_range):
        y -= 1
        if not 0 <= y < height or walls[x, y] or boxes[x, y] != -1:
            break
        elif (x, y) == (pos.x, pos.y):
            return True
    return False

def safe_path(pos: Position) -> bool:
    pass

def deadly_pos(pos: Position, countdown: int) -> bool:
    for bomb in opponent_bombs:
        if bomb.countdown == countdown and bomb_kills(pos, bomb):
            return True
    return False

def is_safe_path(start: Position, end: Position) -> bool:
    queue: deque = deque([(start, 0)])
    visited: set = {(start.x, start.y)}
    while queue:
        pos, countdown = queue.popleft()
        if pos == end:
            return True
        for dx, dy in DIRECTIONS:
            new_pos = Position(pos.x + dx, pos.y + dy)
            if (new_pos.x, new_pos.y) in visited or not in_grid(new_pos.x, new_pos.y) or walls[new_pos.x, new_pos.y] or boxes[new_pos.x, new_pos.y] != -1:
                continue
            if deadly_pos(pos=new_pos, countdown=countdown):
                continue
            queue.append((new_pos, countdown + 1))
            visited.add((new_pos.x, new_pos.y))
    return False


def get_player(player_id: int) -> Optional[Player]:
    player_list = [p for p in players if p.id == player_id]
    return player_list[0] if player_list else None


in_grid = lambda x, y: 0 <= x < width and 0 <= y < height

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
PLAYER = 0
BOMB = 1
ITEM = 2
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

width, height, my_id = [int(i) for i in input().split()]
idebug(width, height, my_id)

players: List[Player] = []

item_collect: bool = False
bomb_plant: bool = False

game_turn: int = 0

# game loop
while True:
    boxes: array = zeros(shape=(width, height), dtype=int)
    walls: array = zeros(shape=(width, height), dtype=int)
    t_boxes = boxes.T
    bombs: List[Bomb] = []
    items: List[Item] = []
    for i in range(height):
        row = input()
        idebug(row)
        for j, value in enumerate(list(row)):
            boxes[j, i] = -1
            walls[j, i] = 0
            if value == '.':
                pass
            elif value == 'X':
                walls[j, i] = 1
            else:
                boxes[j, i] = int(value)

    tic = perf_counter()

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
        elif entity_type == BOMB:
            bombs.append(Bomb(owner=owner, pos=pos, countdown=param_1, range=param_2))
        else:
            items.append(Item(type=ItemType(param_2), pos=pos))

    player: Player = [p for p in players if p.id == my_id][0]
    opponent: Player = [p for p in players if p.id != my_id][0]

    my_bombs: List[Bomb] = [b for b in bombs if b.owner == my_id]
    opponent_bombs: List[Bomb] = [b for b in bombs if b.owner != my_id]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    available_moves: List[Position] = [Position(x, y) for x in range(width) for y in range(height)
                                       if not walls[x, y] and boxes[x, y] == -1 and is_safe_path(player.pos, Position(x, y))]  # and not Position(x, y).is_bomb(my_bombs)]

    if player.target:
        debug(f'game turn = {game_turn}')
        debug(f'player moving to {player.target}')
        debug(f'item collect = {item_collect}')
        debug(f'bomb plant = {bomb_plant}')

    if items and not bomb_plant:
        if not player.target:
            xtra_bomb_items: List[Item] = [i for i in items if i.type == ItemType.XTRA_BOMB and is_safe_path(player.pos, i.pos)]
            xtra_range_items: List[Item] = [i for i in items if i.type == ItemType.XTRA_RANGE and is_safe_path(player.pos, i.pos)]
            closest_xtra_bomb_item: Item = min(xtra_bomb_items, key=lambda i: i.pos.dist(player.pos)) if xtra_bomb_items else None
            closest_xtra_range_item: Item = min(xtra_range_items, key=lambda i: i.pos.dist(player.pos)) if xtra_range_items else None
            if player.bombs < 3 and closest_xtra_bomb_item:
                player.target = closest_xtra_bomb_item.pos
                item_collect: bool = True
            elif player.b_range < 6 and closest_xtra_range_item:
                player.target = closest_xtra_range_item.pos
                item_collect: bool = True
        elif player.pos == player.target:
            player.target = None
            item_collect: bool = False
        if item_collect:
            print(f'MOVE {player.target}')
    else:
        item_collect = False

    if not item_collect:
        if player.bombs:
            if player.target:
                if player.pos == player.target:
                    print(f'BOMB {player.pos} BOMB {player.pos}')
                    available_moves.remove(player.target)
                    player.target = None
                    bomb_plant = False
                else:
                    print(f'MOVE {player.target}')
            else:
                bomb_candidates = [(p, bomb_damage(player, p, bombs)) for p in available_moves]
                bomb_candidates.sort(key=lambda x: x[1], reverse=True)
                # player.target = max(available_moves, key=lambda p: bomb_damage(player, p, bombs) / (1 + p.dist(player.pos)))
                player.target = max(available_moves, key=lambda p: bomb_damage(player, p, bombs))
                bomb_plant = True
                print(f'MOVE {player.target}')
        else:
            if opponent_bombs:
                best_move: Position = max(available_moves, key=lambda p: sum([p.dist(b.pos) for b in opponent_bombs]))
                print(f'MOVE {best_move}')
            else:
                move: Position = choice(available_moves)
                print(f'MOVE {move}')

    game_turn += 1
    debug(f'elapsed time = {round((perf_counter() - tic) * 100, 2)} ms')
