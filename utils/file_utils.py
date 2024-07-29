from typing import Iterable


def read_file(file_name: str) -> Iterable[list[str]]:
    with open(file_name) as f:
        for line in f:
            yield line.strip().split(",")


def append_to_file(file_name: str, txt: str) -> None:
    with open(file_name, "a") as f:
        f.write(txt)
