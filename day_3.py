import re
import utils


def prep_data(input_data: str) -> str:
    return input_data.strip()


def calculate_sum_of_product(input_data: str) -> int:
    data = prep_data(input_data)
    matches = re.findall(r"mul\(([0-9]+),([0-9]+)\)", data)
    return sum([int(a) * int(b) for a, b in matches])


def calculate_sum_of_product_extra(input_data: str) -> int:
    data = prep_data(input_data)
    parts = data.split("do()")  # split do's
    do_parts = [part.split("don't()")[0] for part in parts]  # remove don'ts
    rejoined = "".join(do_parts)
    return calculate_sum_of_product(rejoined)


def test_case():
    input_data = """
        xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
    """
    assert calculate_sum_of_product(input_data) == 161
    input_data = """
        xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
    """
    assert calculate_sum_of_product_extra(input_data) == 48


if __name__ == "__main__":
    test_case()
    input_data = utils.get_input(day=3)
    answer = calculate_sum_of_product(input_data)
    print(f"Part1: {answer}")
    answer = calculate_sum_of_product_extra(input_data)
    print(f"Part2: {answer}")
