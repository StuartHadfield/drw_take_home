import os

from core.constants import INPUT_FILE, OUTPUT_FILE
from core.drw_tetris_processor import process_line
from utils.file_utils import read_file


def main() -> None:
    """
    Main function to read input data, process each line, and output the results.
    """
    input_data = read_file(INPUT_FILE)
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    for line in input_data:
        process_line(line)


if __name__ == "__main__":
    main()
