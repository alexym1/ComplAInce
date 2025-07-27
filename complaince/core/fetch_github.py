"""Generate instructions for Github API"""

import ast
import os
from tempfile import TemporaryDirectory

from git import Repo
from github import Auth, Github

from complaince.tools.cartography_api import CartographyAPI
from complaince.tools.cartography_history import GitHistory
from complaince.tools.cartography_repository import CartographyRepo


def clone_github_repository(repo_name: str, temp_dir: str) -> str:
    """
    Clone a Github repository.

    Parameters
    ----------
    repo_name
        Github repository name in the format "owner/repo"

    temp_dir
        Temporary directory to clone the repository

    Returns
    -------
    Path of the github directory
    """
    repo_dir = os.path.join(temp_dir, 'agent-task')

    if os.path.exists(repo_dir):
        os.system(f'rm -rf {repo_dir}')

    if os.getenv("GITHUB_TOKEN") is None:
        github = Github()
    else:
        auth = Auth.Token(str(os.getenv("GITHUB_TOKEN")))
        github = Github(auth=auth)

    repo = github.get_repo(repo_name)
    repo_clone = Repo.clone_from(repo.clone_url, repo_dir)

    return repo_clone.working_tree_dir


def map_github_repository(repo_name: str) -> None:
    """
    Build and plot the tree structure of a repository.

    Parameters
    ----------
    repo_name
        Full name of the repository in the format "owner/repo"

    output_png
        The output png file to save the plot
    """
    temp_dir = TemporaryDirectory()
    repo_path = clone_github_repository(repo_name, temp_dir.name)

    # Cartography the Repository
    map_repo = CartographyRepo()
    map_repo.build_tree_from_directory(repo_path)
    map_repo.plot(output_png="treemap.png")

    # Cartography the API
    map_api = CartographyAPI()
    contents = map_api.search_code_from_directory(repo_path)

    if len(contents) > 0:
        for item in range(len(contents)):
            with open(contents[item]["path"], "r", encoding="utf-8") as f:
                file_content = ast.parse(f.read())

            map_api.visit(file_content)
            map_api.plot_api(output_png=str(item) + "api.png")

    # Cartography the git history
    repo = GitHistory()
    git_history = repo.git_history_from_local(path=repo_path, n_commits=20)
    repo.plot_history(git_history, "git_history.png")
