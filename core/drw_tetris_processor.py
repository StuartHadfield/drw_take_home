from core.constants import GRID_HEIGHT, GRID_WIDTH, OUTPUT_FILE, SHAPES
from utils.file_utils import append_to_file


def can_place_piece(
    grid: list[list[int]],
    shape: list[tuple[int, int]],
    start_row: int,
    col: int,
) -> bool:
    """
    Checks if a given shape can be placed on the grid at the specified starting row and column.

    Args:
        grid (list[list[int]]): The game grid.
        shape (list[tuple[int, int]]): The shape to be placed, defined as a list of (dy, dx) offsets.
        start_row (int): The starting row index for the shape.
        col (int): The column index for the shape.

    Returns:
        bool: True if the shape can be placed, False otherwise.
    """
    for dy, dx in shape:
        if (
            start_row + dy >= GRID_HEIGHT
            or col + dx >= GRID_WIDTH
            or col + dx < 0
            or grid[start_row + dy][col + dx] == 1
        ):
            return False
    return True


def drop_piece(grid: list[list[int]], shape: list[tuple[int, int]], col: int) -> None:
    """
    Attempts to drop a shape in the specified column of the grid, and places its
    values at the correct corresponding positions.

    Args:
        grid (list[list[int]]): The game grid.
        shape (list[tuple[int, int]]): The shape to be dropped, defined as a list of (dy, dx) offsets.
        col (int): The column index to drop the shape.
    """
    piece_height = max(dy for dy, _ in shape) + 1
    piece_width = max(dx for _, dx in shape) + 1

    if col < 0 or col + piece_width > GRID_WIDTH:
        raise ValueError(f"Piece {shape} at column {col} goes out of bounds")

    for row in range(GRID_HEIGHT - piece_height + 1):
        if any(grid[row + dy][col + dx] == 1 for dy, dx in shape):
            place_piece(grid, shape, row - 1, col)
            break
    else:
        place_piece(grid, shape, GRID_HEIGHT - piece_height, col)

    clear_filled_rows(grid)


def place_piece(
    grid: list[list[int]],
    shape: list[tuple[int, int]],
    row: int,
    col: int,
) -> None:
    """
    Places a shape on the grid at the specified row and column.

    Args:
        grid (list[list[int]]): The game grid.
        shape (list[tuple[int, int]]): The shape to be placed, defined as a list of (dy, dx) offsets.
        row (int): The row index to place the shape.
        col (int): The column index to place the shape.
    """
    if row < 0:
        raise ValueError(f"Cannot place piece {shape} at row {row}, column {col}")
    for dy, dx in shape:
        grid[row + dy][col + dx] = 1


def clear_filled_rows(grid: list[list[int]]) -> None:
    """
    Clears filled rows from the grid and shifts the remaining rows down.

    Args:
        grid (list[list[int]]): The game grid.
    """
    new_grid = [row for row in grid if sum(row) != GRID_WIDTH]
    num_cleared = GRID_HEIGHT - len(new_grid)
    for _ in range(num_cleared):
        new_grid.insert(0, [0] * GRID_WIDTH)
    grid[:] = new_grid


def get_height(grid: list[list[int]]) -> int:
    """
    Calculates the height of the grid, defined as the number of non-empty rows.

    Args:
        grid (list[list[int]]): The game grid.

    Returns:
        int: The height of the grid.
    """
    return sum(1 for row in grid if any(row))


def process_line(line: list[str]) -> None:
    """
    Processes a line of input, dropping each piece described in the line onto the grid, and writes
    the output to the defined output file.

    Args:
        grid (list[list[int]]): The game grid.
        line list(str): The input line describing the pieces to be dropped.
    """
    grid = generate_empty_grid()

    for piece in line:
        piece_letter = piece[0]
        if piece_letter not in SHAPES.keys():
            raise ValueError(f"Unknown piece: {piece_letter}")
        shape = SHAPES[piece_letter]
        col = int(piece[1:])
        drop_piece(grid, shape, col)

    height = get_height(grid)
    append_to_file(OUTPUT_FILE, f"{height}\n")


def generate_empty_grid() -> list[list[int]]:
    """
    Creates an empty grid.

    Returns:
        list[list[int]]: A new empty grid.
    """
    return [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
