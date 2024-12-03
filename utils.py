from pathlib import Path


def get_input(day: int, part: int = 1) -> str:
    return Path(f"day_{day}_input_{part}.txt").read_text()
