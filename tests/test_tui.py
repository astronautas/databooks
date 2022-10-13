import io
from importlib import resources
from textwrap import dedent

from rich.console import Console, ConsoleRenderable

from databooks import JupyterNotebook

with resources.path("tests.files", "demo.ipynb") as nb_path:
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
0.9995123767309688
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
  File "/var/folders/_r/_8qwqbqn4_gdj4m3gb6_t05400
00gn/T/ipykernel_3501/1516912967.py", line 1
    throw error
          ^
SyntaxError: invalid syntax
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
0.9995123767309688
In [3]:
╭────────────────────────────────────────────────╮
│ print("notebooks + git ❤️")                     │
╰────────────────────────────────────────────────╯
notebooks + git ❤️

In [4]:
╭────────────────────────────────────────────────╮
│ throw error                                    │
╰────────────────────────────────────────────────╯
  File "/var/folders/_r/_8qwqbqn4_gdj4m3gb6_t05400
00gn/T/ipykernel_3501/1516912967.py", line 1
    throw error
          ^
SyntaxError: invalid syntax
╭────────────────────────────────────────────────╮
│ This is a raw cell! 🚀                         │
╰────────────────────────────────────────────────╯
"""
        )
    )
