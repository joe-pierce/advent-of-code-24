import utils
import re


def parse_input(input_data: str) -> tuple[list[tuple[int, int]], list[list[int]]]:
    rule_pattern = "([0-9]+)\\|([0-9]+)"
    rules = re.findall(rule_pattern, input_data)
    rules = [(int(x), int(y)) for x, y in rules]
    updates_block = input_data.split("\n\n")[1]
    updates = []
    for update in updates_block.strip().split("\n"):
        updates.append([int(i) for i in update.strip().split(",")])
    return rules, updates

class Validator:
    #TODO: Need to change this to only have orders for explicitly ordered pairs,
    # maybe just simplify and validate against each pair
    def __init__(self, rules:tuple[list[tuple[int, int]]])-> None:
        self.rules = rules
    
    def is_valid(self, values: list[int])-> bool:
        for lower, upper in self.rules:
            if lower in values and upper in values:
                if values.index(upper) < values.index(lower):
                    return False
        return True
    
    def order(self, values: list[int])-> list[int]:
        while not self.is_valid(values):
            for lower, upper in self.rules:
                if lower in values and upper in values:
                    if values.index(upper) < values.index(lower):
                        values[values.index(lower)] = upper
                        values[values.index(upper)] = lower

        return values


def calculate_sum_of_correct_mid_values(input_data: str) -> int:
    rules, updates = parse_input(input_data)
    validator = Validator(rules)
    mid_points = []
    for update in updates:
        if validator.is_valid(update):
            mid_point = update[len(update) // 2]
            mid_points.append(mid_point)
    return sum(mid_points)


def calculate_sum_of_incorrect_mid_values(input_data: str) -> int:
    rules, updates = parse_input(input_data)
    validator = Validator(rules)
    mid_points = []
    for update in updates:
        if validator.is_valid(update):
            continue
        correct_update = validator.order(update)
        mid_point = correct_update[len(correct_update) // 2]
        mid_points.append(mid_point)
    return sum(mid_points)




def test_case():
    input_data = """
        47|53
        97|13
        97|61
        97|47
        75|29
        61|13
        75|53
        29|13
        97|29
        53|29
        61|53
        97|53
        61|29
        47|13
        75|47
        97|75
        47|61
        75|61
        47|29
        75|13
        53|13

        75,47,61,53,29
        97,61,53,29,13
        75,29,13
        75,97,47,61,53
        61,13,29
        97,13,75,29,47
    """
    assert calculate_sum_of_correct_mid_values(input_data) == 143
    assert calculate_sum_of_incorrect_mid_values(input_data) == 123


if __name__ == "__main__":
    test_case()
    input_data = utils.get_input(day=5)
    answer = calculate_sum_of_correct_mid_values(input_data)
    print(f"Part1: {answer}")
    answer = calculate_sum_of_incorrect_mid_values(input_data)
    print(f"Part2: {answer}")
