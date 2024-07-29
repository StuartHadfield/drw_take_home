from unittest.mock import call, patch

from pytest import raises

from core.constants import GRID_HEIGHT, GRID_WIDTH, OUTPUT_FILE, SHAPES
# Assuming the module is named 'tetris', and we import the functions from it
from core.drw_tetris_processor import (can_place_piece, clear_filled_rows,
                                       drop_piece, generate_empty_grid,
                                       get_height, process_line)


def test_can_place_piece():
    shape = SHAPES["Q"]
    grid = generate_empty_grid()
    assert can_place_piece(grid, shape, 0, 0) is True
    grid[0][0] = 1
    assert can_place_piece(grid, shape, 0, 0) is False


def test_drop_piece():
    expected = {
        "Q": [
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "Z": [
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        ],
        "S": [
            [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "T": [
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "I": [
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        ],
        "L": [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "J": [
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
    }

    for shape, expected_grid in expected.items():
        grid = generate_empty_grid()
        drop_piece(grid, SHAPES[shape], 0)
        full_grid = [
            [0] * GRID_WIDTH for _ in range(GRID_HEIGHT - len(expected_grid))
        ] + expected_grid
        assert grid == full_grid


def test_clear_filled_rows():
    grid = generate_empty_grid()
    grid[0] = [1] * GRID_WIDTH
    grid[1][0] = 1
    clear_filled_rows(grid)
    expected_grid = [
        [0] * GRID_WIDTH,
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ] + [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT - 2)]
    assert grid == expected_grid


def test_get_height():
    grid = generate_empty_grid()
    grid[0][0] = 1
    grid[2][0] = 1
    assert get_height(grid) == 2


@patch("core.drw_tetris_processor.append_to_file")
def test_process_line(mock_append_to_file):
    lines_and_heights = [
        (["I0", "I4", "Q8"], 1),
        (["I0", "L2", "T4"], 4),
        (["Q0", "I2", "I6", "I0", "I6", "I6", "Q2", "Q4"], 3),
        (["Q0", "Q0", "Q0", "Q0", "Q0"], 10),
    ]

    for line, height in lines_and_heights:
        process_line(line)
        expected_calls = [call(OUTPUT_FILE, f"{height}\n")]
        mock_append_to_file.assert_has_calls(expected_calls, any_order=True)


def test_place_too_many_pieces_raises_error():
    with raises(ValueError) as exc:
        process_line(["Q0"] * 20000)

    assert (
        str(exc.value)
        == "Cannot place piece [(0, 0), (0, 1), (1, 0), (1, 1)] at row -1, column 0"
    )


def test_place_out_of_grid_raises_error():
    with raises(ValueError) as exc:
        process_line(["Q25"])

    assert (
        str(exc.value)
        == "Piece [(0, 0), (0, 1), (1, 0), (1, 1)] at column 25 goes out of bounds"
    )


def test_place_unknown_shape_raises_error():
    with raises(ValueError) as exc:
        process_line(["H0"])

    assert str(exc.value) == "Unknown piece: H"
