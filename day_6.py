import utils
import re
from enum import Enum
import numpy as np


class Orient(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


class Game:
    def __init__(self, input_data: str):
        self.parse_input(input_data)

    def parse_input(self, input_data: str):
        self.key = {".": 0, "#": 1, "^": 2}
        self.map = np.array(
            [
                [self.key[char] for char in s.strip()]
                for s in input_data.strip().split("\n")
            ]
        )
        self.original_map = self.map.copy()
        self.current_position = tuple(i[0] for i in np.where(self.map == 2))
        self.current_orient = Orient.UP
        self.visited_positions = set()
        self.positions_and_orients = set()
        self.visited_positions.add(self.current_position)
        self.positions_and_orients.add((self.current_position, self.current_orient))
        self.endless_loop = False

    def run(self):
        while self.current_position is not None and not self.endless_loop:
            self.move()
            if (
                self.current_position,
                self.current_orient,
            ) in self.positions_and_orients:
                self.endless_loop = True
            self.positions_and_orients.add((self.current_position, self.current_orient))

    def move(self):
        move_vector = np.array(self.current_orient.value)
        new_position = tuple(self.current_position + move_vector)
        if any([i < 0 for i in new_position]):
            # out of bounds
            self.current_position = None
            return
        try:
            if self.map[new_position] != 1:
                # Room to move
                self.current_position = new_position
                self.visited_positions.add(self.current_position)
            else:
                # No room to move, turn to right
                self.turn()

        except IndexError:
            # out of bounds
            self.current_position = None
            return

    def turn(self):
        match self.current_orient:
            case Orient.UP:
                self.current_orient = Orient.RIGHT
            case Orient.RIGHT:
                self.current_orient = Orient.DOWN
            case Orient.DOWN:
                self.current_orient = Orient.LEFT
            case Orient.LEFT:
                self.current_orient = Orient.UP

    def reset(self):
        self.map = self.original_map.copy()
        self.current_position = tuple(i[0] for i in np.where(self.map == 2))
        self.current_orient = Orient.UP
        self.visited_positions = set()
        self.positions_and_orients = set()
        self.visited_positions.add(self.current_position)
        self.positions_and_orients.add((self.current_position, self.current_orient))
        self.endless_loop = False


def calculate_positions(input_data: str):
    game = Game(input_data)
    game.run()
    return len(game.visited_positions)


def calculate_obstruction_positions(input_data: str):
    game = Game(input_data)
    game.run()
    potential_positions = np.array(list(game.visited_positions)).T
    endless_loop_count = 0
    position_count = len(potential_positions[0])
    for i, position in enumerate(zip(*potential_positions)):
        if game.map[position] == 2:
            continue  # can't add obstruction at starting point
        game.map[position] = 1
        game.run()
        if game.endless_loop:
            endless_loop_count += 1
        game.reset()
        print(
            f"{i+1} of {position_count} runs finished - endless loops: {endless_loop_count}"
        )

    return endless_loop_count


def test_case():
    input_data = """
        ....#.....
        .........#
        ..........
        ..#.......
        .......#..
        ..........
        .#..^.....
        ........#.
        #.........
        ......#...
    """
    assert calculate_positions(input_data) == 41
    assert calculate_obstruction_positions(input_data) == 6


if __name__ == "__main__":
    test_case()
    input_data = utils.get_input(day=6)
    answer = calculate_positions(input_data)
    print(f"Part1: {answer}")
    answer = calculate_obstruction_positions(input_data)
    print(f"Part2: {answer}")
