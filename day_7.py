import utils
import re
import itertools
import numpy as np


class Calibrator:
    def __init__(self, input_line: str):
        line = input_line.strip()
        partition = line.partition(":")
        self.answer = int(partition[0])
        self.parts = [int(part) for part in partition[2].strip().split(" ")]

    def is_valid(self, with_concat: bool = False):
        number_of_operations = len(self.parts) - 1
        operators = [np.sum, np.prod]
        if with_concat:
            operators.append(lambda arr: np.char.add(*arr.astype(str)).astype(int))
        operator_combos = itertools.product(operators, repeat=number_of_operations)
        for operator_combo in operator_combos:
            result = self.parts[0]
            for part, operator in zip(self.parts[1:], operator_combo):
                result = operator(np.array([result, part]))
            if result == self.answer:
                return True

        return False


def sum_correct_answers(input_data: str, **kwargs):
    result = 0
    for line in input_data.strip().split("\n"):
        calibrator = Calibrator(line)
        if calibrator.is_valid(**kwargs):
            result += calibrator.answer
    return result


def test_case():
    input_data = """
        190: 10 19
        3267: 81 40 27
        83: 17 5
        156: 15 6
        7290: 6 8 6 15
        161011: 16 10 13
        192: 17 8 14
        21037: 9 7 18 13
        292: 11 6 16 20
    """
    assert sum_correct_answers(input_data) == 3749
    assert sum_correct_answers(input_data, with_concat=True) == 11387


if __name__ == "__main__":
    test_case()
    input_data = utils.get_input(day=7)
    answer = sum_correct_answers(input_data)
    print(f"Part1: {answer}")
    answer = sum_correct_answers(input_data, with_concat=True)
    print(f"Part2: {answer}")
