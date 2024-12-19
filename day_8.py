import utils
import re
import itertools
import math
import numpy as np
from shapely.geometry import LineString


class AntennaMap:
    def __init__(self, input_data: str):
        self.key = {".": 0}
        self.unique_chars = list(
            set([char for char in input_data if char not in " .\n"])
        )
        for i, char in enumerate(self.unique_chars):
            self.key[char] = i + 1

        self.map = np.array(
            [
                [self.key[char] for char in s.strip()]
                for s in input_data.strip().split("\n")
            ]
        )
        self.max_y, self.max_x = self.map.shape
        self.max_y -= 1
        self.max_x -= 1
        self.get_antenna_pairs()

    def get_antenna_pairs(self):
        self.antenna_pairs = []
        for char in self.unique_chars:
            coords = list(zip(*np.where(self.map == self.key[char])))
            for (y, x), (j, i) in itertools.combinations(coords, 2):
                line = LineString([[x, self.max_y - y], [i, self.max_y - j]])
                self.antenna_pairs.append(line)

    @property
    def antinodes(self):
        antinodes = set()
        for antenna_pair in self.antenna_pairs:
            start, end = map(np.array, antenna_pair.coords)
            vector_diff = end - start
            antinodes.update([tuple(end + vector_diff), tuple(start - vector_diff)])

        return self.validate_antinodes(antinodes)

    def validate_antinodes(self, antinodes):
        # Remove OOB antinodes
        valid_antinodes = []
        for antinode in antinodes:
            if (
                (antinode[0] < 0)
                or (antinode[0] > self.max_x)
                or (antinode[1] < 0)
                or (antinode[1] > self.max_y)
            ):
                continue
            valid_antinodes.append(antinode)

        return valid_antinodes

    @property
    def special_antinodes(self):
        antinodes = set()
        for antenna_pair in self.antenna_pairs:
            start, end = map(np.array, antenna_pair.coords)
            vector_diff = end - start
            unit_vector = vector_diff / math.gcd(*map(int, vector_diff))
            for i in range(max(self.map.shape)):
                antinodes.add(tuple(start + (unit_vector * i)))
                antinodes.add(tuple(start - (unit_vector * i)))

        return self.validate_antinodes(antinodes)


def count_antinodes(input_data: str) -> int:
    antenna_map = AntennaMap(input_data)
    return len(antenna_map.antinodes)


def count_part_two_antinodes(input_data: str) -> int:
    antenna_map = AntennaMap(input_data)
    return len(antenna_map.special_antinodes)


def test_case():
    input_data = """
        ............
        ........0...
        .....0......
        .......0....
        ....0.......
        ......A.....
        ............
        ............
        ........A...
        .........A..
        ............
        ............
    """
    assert count_antinodes(input_data) == 14
    assert count_part_two_antinodes(input_data) == 34


if __name__ == "__main__":
    test_case()
    input_data = utils.get_input(day=8)
    answer = count_antinodes(input_data)
    print(f"Part1: {answer}")
    answer = count_part_two_antinodes(input_data)
    print(f"Part2: {answer}")
