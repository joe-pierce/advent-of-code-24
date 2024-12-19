import utils
import numpy as np
from numpy.typing import NDArray
from scipy.ndimage import generic_filter


def prep_data(input_data: str) -> NDArray:
    map_chars = {"X": 1, "M": 2, "A": 3, "S": 4}
    return np.array(
        [
            [map_chars.get(char, 0) for char in line.strip()]
            for line in input_data.strip().split("\n")
        ]
    )


def horizontal(idx, row_size):
    idxs = np.array([idx, idx + 1, idx + 2, idx + 3])
    return idxs[:, np.where((idxs[0] % row_size) <= row_size - 4)[0]]


def vertical(idx, row_size):
    return (np.array([row_size] * 4) * np.array([0, 1, 2, 3]))[:, np.newaxis] + idx


def diagonal_up(idx, row_size):
    idxs = (
        np.array([row_size] * 4) * np.array([0, -1, -2, -3]) + np.array([0, 1, 2, 3])
    )[:, np.newaxis] + idx
    return idxs[:, np.where((idxs[0] % row_size) <= row_size - 4)[0]]


def diagonal_down(idx, row_size):
    idxs = (np.array([row_size] * 4) * np.array([0, 1, 2, 3]) + np.array([0, 1, 2, 3]))[
        :, np.newaxis
    ] + idx
    return idxs[:, np.where((idxs[0] % row_size) <= row_size - 4)[0]]


def X(idx, row_size):
    idxs = np.array(
        [
            idx,
            idx + 2,
            idx + row_size + 1,
            idx + (2 * row_size),
            idx + (2 * row_size) + 2,
        ]
    )
    return idxs[:, np.where((idxs[0] % row_size) <= row_size - 3)[0]]


def find_xmas(input_data: str) -> int:
    arr = prep_data(input_data)
    row_size = arr.shape[1]
    arr = arr.flatten()
    orients = {
        "horizontal": lambda idx: horizontal(idx, row_size),
        "vertical": lambda idx: vertical(idx, row_size),
        "diagonal_up": lambda idx: diagonal_up(idx, row_size),
        "diagonal_down": lambda idx: diagonal_down(idx, row_size),
    }
    total_xmas_count = 0
    for orient, func in orients.items():
        for word, pattern in (
            ("xmas", [1, 2, 3, 4]),
            ("samx", [4, 3, 2, 1]),
        ):
            idxs = func(np.arange(arr.size))
            # clip to bounds
            idxs = idxs[:, np.where(np.all((idxs >= 0) & (idxs < arr.size), axis=0))[0]]
            xmas_count = int(np.sum(np.all(arr[idxs].T == pattern, axis=1)))
            print(f"{xmas_count} {word} found in {orient} orient")
            total_xmas_count += xmas_count

    return total_xmas_count


def find_X_mas(input_data: str) -> int:
    arr = prep_data(input_data)
    row_size = arr.shape[1]
    arr = arr.flatten()
    total_x_mas_count = 0

    for word, pattern in (
        ("mmass", [2, 2, 3, 4, 4]),
        ("ssamm", [4, 4, 3, 2, 2]),
        ("msams", [2, 4, 3, 2, 4]),
        ("smasm", [4, 2, 3, 4, 2]),
    ):
        idxs = X(np.arange(arr.size), row_size)
        # clip to bounds
        idxs = idxs[:, np.where(np.all((idxs >= 0) & (idxs < arr.size), axis=0))[0]]
        x_mas_count = int(np.sum(np.all(arr[idxs].T == pattern, axis=1)))
        print(f"{x_mas_count} {word} found in X-mas orient")
        total_x_mas_count += x_mas_count

    return total_x_mas_count


def test_case():
    input_data = """
        MMMSXXMASM
        MSAMXMSMSA
        AMXSXMAAMM
        MSAMASMSMX
        XMASAMXAMM
        XXAMMXXAMA
        SMSMSASXSS
        SAXAMASAAA
        MAMMMXMMMM
        MXMXAXMASX
    """
    assert find_xmas(input_data) == 18
    assert find_X_mas(input_data) == 9


if __name__ == "__main__":
    test_case()
    input_data = utils.get_input(day=4)
    answer = find_xmas(input_data)
    print(f"Part1: {answer}")
    answer = find_X_mas(input_data)
    print(f"Part2: {answer}")
