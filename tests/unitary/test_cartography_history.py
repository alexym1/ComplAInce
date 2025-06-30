"""Test tools module."""

import os
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from complaince.tools.cartography_history import GitHistory


@pytest.fixture(scope="module")
def temp_dir():
    TEMP_DIR = TemporaryDirectory(prefix="history_")
    yield Path(TEMP_DIR.name)

@pytest.fixture(scope="module")
def repo():
    yield GitHistory()

@pytest.fixture(scope="module")
def history(repo):
    yield repo.git_history_from_local(n_commits=10)


def test_git_history_from_local(history):
    assert history.shape[0] <= 10
    assert history.shape[1] == 5
    assert history.columns.tolist() == ["Description", "Date", "Author", "Commit", "Branch"]

def test_git_history_from_github(repo):
    git_logs = repo.git_history_from_github("alexym1/booklet", n_commits=10)
    assert git_logs.shape[0] <= 10
    assert git_logs.shape[1] == 5
    assert git_logs.columns.tolist() == ["Description", "Date", "Author", "Commit", "Branch"]

def test_plot_history(repo, history, temp_dir):
    empty_folder = os.listdir(str(temp_dir))
    repo.plot_history(history, output_png = os.path.join(temp_dir, "history.png"))
    full_folder = os.listdir(str(temp_dir))
    assert empty_folder == []
    assert full_folder == ["history.png"]
