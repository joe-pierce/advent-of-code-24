import utils
import numpy as np


class DiskMap:
    def __init__(self, input_data: str):
        data = [int(char) for char in input_data]
        if len(data) % 2 == 1:
            data.append(0)

        arr = np.array(data).reshape((-1, 2))

        disk = []
        for index, (files, spaces) in enumerate(arr):
            disk.extend([index] * files)
            disk.extend([(index + 1) * -1] * spaces)

        self.disk = disk

    def defrag(self) -> None:
        for position, item in enumerate(self.disk):
            if item >= 0:
                continue
            while (last_value := self.disk.pop()) < 0:
                continue
            try:
                self.disk[position] = last_value
            except IndexError:
                self.disk.append(last_value)
                break

    def whole_block_defrag(self) -> None:
        # Gonna just brute force it
        disk_arr = np.array(self.disk)
        unique_files = sorted(set(self.disk), reverse=True)
        min_value = int(disk_arr.min())
        unique_spaces = list(range(-1, min_value - 1, -1))
        for file in unique_files:
            if file < 0:
                break
            print(f"processing file {file}")
            file_size = np.sum(disk_arr == file)
            file_index = np.where(disk_arr == file)[0][0]
            for space in unique_spaces[::]:
                space_size = np.sum(disk_arr == space)
                if space_size == 0:
                    unique_spaces.remove(space)
                    continue
                space_index = np.where(disk_arr == space)[0][0]
                if space_index > file_index:
                    break
                if space_size < file_size:
                    continue
                self.disk[space_index : space_index + file_size] = [file] * file_size
                self.disk[file_index : file_index + file_size] = [
                    min_value - 1
                ] * file_size
                disk_arr = np.array(self.disk)
                break

        pass

    def checksum(self) -> int:
        checksum = 0
        for position, item in enumerate(self.disk):
            if item < 0:
                continue
            checksum += position * item

        return checksum


def calculate_checksum(input_data: str, whole_blocks: bool = False) -> int:
    disk_map = DiskMap(input_data)
    disk_map.whole_block_defrag() if whole_blocks else disk_map.defrag()
    return disk_map.checksum()


def test_case():
    input_data = "2333133121414131402"
    assert calculate_checksum(input_data) == 1928
    assert calculate_checksum(input_data, whole_blocks=True) == 2858


if __name__ == "__main__":
    test_case()
    input_data = utils.get_input(day=9)
    answer = calculate_checksum(input_data)
    print(f"Part1: {answer}")
    answer = calculate_checksum(input_data, whole_blocks=True)
    print(f"Part2: {answer}")
