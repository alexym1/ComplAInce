"""Test tools module."""

import os
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from complaince.tools.cartography_repository import CartographyRepo


@pytest.fixture(scope="module")
def temp_dir():
    TEMP_DIR = TemporaryDirectory(prefix="treemap_")
    yield Path(TEMP_DIR.name)

@pytest.fixture(scope="module")
def lst_tree():
    yield ['.github/workflows/pkgdown.yaml', '.gitignore']

@pytest.fixture(scope="module")
def tree():
    yield CartographyRepo(removed_files = ["site"])


def test_build_tree_from_github(tree):
    lst_tree = tree.build_tree_from_github("alexym1/booklet")
    assert isinstance(lst_tree, list)
    assert 'renv.lock' in lst_tree
    assert 'R/' in lst_tree
    assert '.Rbuildignore' in lst_tree

def test_display_tree(tree):
    tree.build_tree_from_directory()
    displayed_tree = tree.display_tree()
    assert isinstance(displayed_tree, str)

def test_plot(tree, temp_dir):
    empty_folder = os.listdir(str(temp_dir))
    tree.plot(output_png = os.path.join(temp_dir, "treemap.png"))
    full_folder = os.listdir(str(temp_dir))
    assert empty_folder == []
    assert full_folder == ["treemap.png"]
