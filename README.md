### Running the script

Ensure you have a `input.txt` in the source directory. The application does no intelligent matching on a path, it just looks for a file in the execution dir.

The code is designed to be executed using Python 3.12.

It can be executed as:

```
python main.py
```

By default it will output a file called `output.txt`. This file will be cleared & repopulated on each run.

### Running tests

To run tests, you will need pytest:

```
pip install pytest
```

You can then execute the tests:


```
pytest tests/
```

### Description

DRW Take Home Test implementation for a variant of Tetris.