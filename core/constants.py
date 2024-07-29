from typing import Final

INPUT_FILE: Final[str] = "input.txt"
OUTPUT_FILE: Final[str] = "output.txt"

SHAPES: Final[dict[str, list[tuple[int, int]]]] = {
    "Q": [(0, 0), (0, 1), (1, 0), (1, 1)],  # 2x2 square
    "Z": [(0, 0), (0, 1), (1, 1), (1, 2)],  # Z shape
    "S": [(1, 0), (1, 1), (0, 1), (0, 2)],  # S shape
    "T": [(0, 0), (0, 1), (0, 2), (1, 1)],  # T shape
    "I": [(0, 0), (0, 1), (0, 2), (0, 3)],  # Horizontal line
    "L": [(0, 0), (1, 0), (2, 0), (2, 1)],  # L shape
    "J": [(0, 1), (1, 1), (2, 1), (2, 0)],  # J shape
}

GRID_WIDTH: Final[int] = 10
GRID_HEIGHT: Final[int] = 100
