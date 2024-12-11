import numpy as np
from numpy.typing import NDArray
import utils


def prep_data(input_data: str) -> list[NDArray]:
    return [
        np.array(line.strip().split()).astype(int)
        for line in input_data.strip().split("\n")
    ]


def calculate_safe_count(input_data: str, with_dampener: bool = False) -> int:
    list_of_arr = prep_data(input_data)
    total_count = 0
    for arr in list_of_arr:
        if is_safe(arr):
            total_count += 1
        elif with_dampener:
            if is_safe(np.array([np.delete(arr, i) for i in range(len(arr))])):
                total_count += 1
    return total_count

def is_safe(arr: NDArray)-> bool:
    if arr.ndim ==1:
        arr = arr[np.newaxis, :]
    diff = np.diff(arr)
    report_length = diff.shape[1]
    rule_2_applied = np.where((diff != 0) & (np.abs(diff) < 4), 1, 0)
    result = np.sum(
        np.where(
            (np.sum(rule_2_applied, axis=1) == report_length)
            & (np.abs(np.sum(np.sign(diff), axis=1)) == report_length),
            1,
            0,
        )
    )
    return int(result) > 0

def test_case():
    input_data = """
        7 6 4 2 1
        1 2 7 8 9
        9 7 6 2 1
        1 3 2 4 5
        8 6 4 4 1
        1 3 6 7 9
    """
    assert calculate_safe_count(input_data) == 2
    assert calculate_safe_count(input_data, with_dampener=True) == 4


if __name__ == "__main__":
    test_case()
    input_data = utils.get_input(day=2)
    answer = calculate_safe_count(input_data)
    print(f"Part1: {answer}")
    answer = calculate_safe_count(input_data, with_dampener=True)
    print(f"Part2: {answer}")
