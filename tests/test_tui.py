import io
from importlib import resources
from textwrap import dedent

from rich.console import Console, ConsoleRenderable

from databooks import JupyterNotebook

with resources.path("tests.files", "tui-demo.ipynb") as nb_path:
    nb = JupyterNotebook.parse_file(nb_path)


def render(obj: ConsoleRenderable, width: int = 50) -> str:
    """Render object to string (instead of terminal)."""
    console = Console(file=io.StringIO(), width=width, legacy_windows=False)
    console.print(obj)
    return console.file.getvalue()


def test_code_cell():
    """Prints code cell with no outputs."""
    assert render(nb.cells[1]) == dedent(
        """\
In [1]:
╭────────────────────────────────────────────────╮
│ from random import random  # cell with tags    │
╰────────────────────────────────────────────────╯
"""
    )


def test_code_cell_outputs():
    """Prints code cell with outputs."""
    assert render(nb.cells[2]) == dedent(
        """\
In [2]:
╭────────────────────────────────────────────────╮
│ random()                                       │
╰────────────────────────────────────────────────╯
Out [2]:
0.570736084214906
"""
    )


def test_code_cell_error():
    """Prints code cell with errors."""
    assert render(nb.cells[4]) == dedent(
        """\
In [4]:
╭────────────────────────────────────────────────╮
│ throw error                                    │
╰────────────────────────────────────────────────╯
  Cell In [4], line 1
    throw error
          ^
SyntaxError: invalid syntax
"""
    )


def test_code_cell_df():
    """Prints code cell data frame and has print statement."""
    assert render(nb.cells[6]) == dedent(
        """\
In [5]:
╭────────────────────────────────────────────────╮
│ import pandas as pd                            │
│ import numpy as np                             │
│                                                │
│ print("A dataframe! 🐼")                       │
│ pd.DataFrame(np.random.random((10,3)), columns │
╰────────────────────────────────────────────────╯
A dataframe! 🐼

Out [5]:
       col0      col1      col2
0  0.849474  0.756456  0.268569
1  0.511937  0.357224  0.570879
2  0.836116  0.928280  0.946514
3  0.803129  0.540215  0.335783
4  0.074853  0.661168  0.344527
5  0.299696  0.782420  0.970147
6  0.159906  0.566822  0.243798
7  0.896461  0.174406  0.758376
8  0.708324  0.895195  0.769364
9  0.860726  0.381919  0.329727
"""
    )


def test_md_cell():
    """Prints markdown cell."""
    assert render(nb.cells[0]) == dedent(
        """\
╭────────────────────────────────────────────────╮
│ ╔════════════════════════════════════════════╗ │
│ ║              databooks demo!               ║ │
│ ╚════════════════════════════════════════════╝ │
╰────────────────────────────────────────────────╯
"""
    )


def test_raw_cell():
    """Prints raw cell."""
    assert render(nb.cells[5]) == dedent(
        """\
╭────────────────────────────────────────────────╮
│ This is a raw cell! 🚀                         │
╰────────────────────────────────────────────────╯
"""
    )


def test_notebook():
    """Prints notebook (identical to printing all cells)."""
    assert (
        render(nb)
        == render(nb.cells)
        == dedent(
            """\
╭────────────────────────────────────────────────╮
│ ╔════════════════════════════════════════════╗ │
│ ║              databooks demo!               ║ │
│ ╚════════════════════════════════════════════╝ │
╰────────────────────────────────────────────────╯
In [1]:
╭────────────────────────────────────────────────╮
│ from random import random  # cell with tags    │
╰────────────────────────────────────────────────╯
In [2]:
╭────────────────────────────────────────────────╮
│ random()                                       │
╰────────────────────────────────────────────────╯
Out [2]:
0.570736084214906
In [3]:
╭────────────────────────────────────────────────╮
│ print("notebooks + git ❤️")                     │
╰────────────────────────────────────────────────╯
notebooks + git ❤️

In [4]:
╭────────────────────────────────────────────────╮
│ throw error                                    │
╰────────────────────────────────────────────────╯
  Cell In [4], line 1
    throw error
          ^
SyntaxError: invalid syntax
╭────────────────────────────────────────────────╮
│ This is a raw cell! 🚀                         │
╰────────────────────────────────────────────────╯
In [5]:
╭────────────────────────────────────────────────╮
│ import pandas as pd                            │
│ import numpy as np                             │
│                                                │
│ print("A dataframe! 🐼")                       │
│ pd.DataFrame(np.random.random((10,3)), columns │
╰────────────────────────────────────────────────╯
A dataframe! 🐼

Out [5]:
       col0      col1      col2
0  0.849474  0.756456  0.268569
1  0.511937  0.357224  0.570879
2  0.836116  0.928280  0.946514
3  0.803129  0.540215  0.335783
4  0.074853  0.661168  0.344527
5  0.299696  0.782420  0.970147
6  0.159906  0.566822  0.243798
7  0.896461  0.174406  0.758376
8  0.708324  0.895195  0.769364
9  0.860726  0.381919  0.329727
In [ ]:
╭────────────────────────────────────────────────╮
│                                                │
╰────────────────────────────────────────────────╯
"""
        )
    )
