import numpy as np
from numpy.typing import NDArray
import utils

def prep_data(input_data:str) -> NDArray:
    return np.array(
        [line.strip().split() for line in input_data.strip().split("\n")]
    ).astype(int)

def calculate_distance_between_lists(input_data: str) -> int:
    arr = prep_data(input_data)
    arr = np.sort(arr, 0)
    return int(np.sum(np.abs(np.diff(arr))))

def calculate_similarity_score(input_data: str) -> int:
    arr = prep_data(input_data)
    left_arr = arr[:,0]
    right_arr = arr[:,1]
    return np.sum(np.sum(left_arr[:, np.newaxis]==right_arr, axis=1) * left_arr)
    


def test_case():
    input_data = """
        3   4
        4   3
        2   5
        1   3
        3   9
        3   3
    """
    assert calculate_distance_between_lists(input_data) == 11
    assert calculate_similarity_score(input_data) == 31


if __name__ == "__main__":
    test_case()
    input_data = utils.get_input(day=1)
    answer = calculate_distance_between_lists(input_data)
    print(f"Part1: {answer}")

    answer = calculate_similarity_score(input_data)
    print(f"Part2: {answer}")
