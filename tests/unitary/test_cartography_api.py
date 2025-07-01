"""Test tools module."""

import ast
import os
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from complaince.tools.cartography_api import CartographyAPI


@pytest.fixture(scope="module")
def temp_dir():
    TEMP_DIR = TemporaryDirectory(prefix="api_")
    yield Path(TEMP_DIR.name)

@pytest.fixture(scope="module")
def py_file():
    with open("./data/fake_repo/fastapi_web_app.py", "r", encoding="utf-8") as f:
        yield ast.parse(f.read())

@pytest.fixture(scope="module")
def mapper():
    yield CartographyAPI()


def test_get_api_from_github(mapper):
    contents = mapper.get_api_from_github("marciovrl/fastapi")
    assert len(contents) == 1
    assert contents[0].keys() == {"path", "url", "snippet"}
    assert contents[0]["path"] == "app/main.py"
    assert contents[0]["url"] == "https://github.com/marciovrl/fastapi/blob/master/app/main.py"
    assert isinstance(contents[0]["snippet"], str)

def test_tree_as_string(mapper, py_file):
    mapper.visit(py_file)
    tree_string = mapper.tree_as_string()
    assert isinstance(tree_string, str)

def test_plot_api(mapper, temp_dir):
    empty_folder = os.listdir(str(temp_dir))
    mapper.plot_api(output_png = os.path.join(temp_dir, "api.png"))
    full_folder = os.listdir(str(temp_dir))
    assert empty_folder == []
    assert full_folder == ["api.png"]
