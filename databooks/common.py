"""Common set of miscellaneous functions."""
from itertools import chain
from pathlib import Path
from typing import Iterable, List, Optional

from databooks.logging import get_logger

logger = get_logger(__file__)


def expand_paths(
    paths: List[Path], *, ignore: List[str] = ["!*"], rglob: str = "*.ipynb"
) -> List[Path]:
    """
    Get paths of existing file from list of directory or file paths.

    :param paths: Paths to consider (can be directories or files)
    :param ignore: Glob expressions of files to ignore
    :param rglob: Glob expression for expanding directory paths and filtering out
     existing file paths (i.e.: to retrieve only notebooks)
    :return: List of existing file paths
    """
    filepaths = list(
        chain.from_iterable(
            list(path.rglob(rglob)) if path.is_dir() else [path] for path in paths
        )
    )
    valid_filepaths = [
        p
        for p in filepaths
        if not any(p.match(i) for i in ignore) and p.is_file() and p.match(rglob)
    ]

    if not valid_filepaths:
        logger.debug(
            f"There are no files in {paths} (ignoring {ignore}) that match `{rglob}`."
        )
    return valid_filepaths


def find_common_parent(paths: Iterable[Path]) -> Path:
    """Find common parent amongst several file paths (includes current path)."""
    if not paths:
        raise ValueError(f"Expected non-empty `paths`, got {paths}.")
    return max(set.intersection(*[{*p.resolve().parents, p.resolve()} for p in paths]))


def find_obj(
    obj_name: str, start: Path, finish: Path, is_dir: bool = False
) -> Optional[Path]:
    """
    Recursively find file along directory path, from the end (child) directory to start.

    :param obj_name: File name to locate
    :param start: Start (parent) directory
    :param finish: Finish (child) directory
    :param is_dir: Whether object is a directory or a file
    :return: File path
    """
    if not start.is_dir() or not finish.is_dir():
        raise ValueError("Parameters `start` and `finish` must be directories.")

    if start.resolve() not in [finish, *finish.resolve().parents]:
        logger.debug(
            f"Parameter `start` is not a parent directory of `finish` (for {start} and"
            f" {finish}). Cannot find {obj_name}."
        )
        return None

    is_obj = (finish / obj_name).is_dir() if is_dir else (finish / obj_name).is_file()
    if is_obj:
        return finish / obj_name
    elif finish.samefile(start):
        logger.debug(f"{obj_name} not found between {start} and {finish}.")
        return None
    else:
        return find_obj(
            obj_name=obj_name, start=start, finish=finish.parent, is_dir=is_dir
        )
