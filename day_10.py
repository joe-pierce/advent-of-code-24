import utils
import numpy as np

UP, DOWN, LEFT, RIGHT = ((-1, 0), (1, 0), (0, -1), (0, 1))
ALL_DIRECTIONS = np.array([UP, DOWN, LEFT, RIGHT])[:, :, np.newaxis]


class TrailMap:
    def __init__(self, input_data: str):
        self.map = np.array(
            [[int(i) for i in s.strip()] for s in input_data.strip().split("\n")]
        )
        self.map = np.pad(self.map, pad_width=1, constant_values=-1)
        self.find_trailheads()

    def find_trailheads(self):
        self.trailheads = []
        trailheads = np.array(np.where(self.map == 0))
        for trailhead in trailheads.T:
            valid_positions = trailhead.reshape(2, 1)
            for trail_point in range(1, 10):
                next_steps = (
                    (valid_positions + ALL_DIRECTIONS).transpose(1, 0, 2).reshape(2, -1)
                )
                valid_positions = next_steps[
                    :, np.where(self.map[*next_steps] == trail_point)[0]
                ]
            num_routes = valid_positions.shape[1]
            unique_ends = set([(int(a), int(b)) for a, b in zip(*valid_positions)])
            self.trailheads.append(
                {
                    "start": tuple([int(i) for i in trailhead]),
                    "rating": num_routes,
                    "unique_endpoints": unique_ends,
                    "score": len(unique_ends),
                }
            )


def sum_trailhead_scores(input_data: str):
    trail_map = TrailMap(input_data)
    return sum([trailhead["score"] for trailhead in trail_map.trailheads])


def sum_trailhead_ratings(input_data: str):
    trail_map = TrailMap(input_data)
    return sum([trailhead["rating"] for trailhead in trail_map.trailheads])


def test_case():
    input_data = """
        89010123
        78121874
        87430965
        96549874
        45678903
        32019012
        01329801
        10456732
    """
    assert sum_trailhead_scores(input_data) == 36
    assert sum_trailhead_ratings(input_data) == 81


if __name__ == "__main__":
    test_case()
    input_data = utils.get_input(day=10)
    answer = sum_trailhead_scores(input_data)
    print(f"Part1: {answer}")
    answer = sum_trailhead_ratings(input_data)
    print(f"Part2: {answer}")
