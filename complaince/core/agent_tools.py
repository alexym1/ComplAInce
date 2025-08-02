"""Tools related to the AI agent."""

import ast
import logging
import os
from datetime import datetime
from tempfile import TemporaryDirectory

from git import Repo
from github import Auth, Github
from langchain_core.tools import tool

from complaince.tools.cartography_api import CartographyAPI
from complaince.tools.cartography_history import GitHistory
from complaince.tools.cartography_repository import CartographyRepo

logger = logging.getLogger(__name__)

temp_dir = TemporaryDirectory()

# Create a timestamped output directory
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_dir = f"res_complaince_{timestamp}"
os.makedirs(output_dir, exist_ok=True)


@tool
def clone_github_repository(repo_name: str, temp_dir: str = temp_dir.name) -> str:
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

    logger.info('Repository cloned successfully at %s', repo_clone.working_tree_dir)

    return repo_clone.working_tree_dir


@tool
def map_repo_structure_tool(repo_path: str, output_dir: str = output_dir) -> None:
    """
    Map the folder structure of a repository.

    Parameters
    ----------
    repo_path
        Path to the repository

    output_dir
        Directory to save the output
    """
    map_repo = CartographyRepo()
    map_repo.build_tree_from_directory(repo_path)
    map_repo.plot(output_png=os.path.join(output_dir, "treemap.png"))


@tool
def map_api_structure_tool(repo_path: str, output_dir: str = output_dir) -> list[str]:
    """
    Map the folder structure of a repository.

    Parameters
    ----------
    repo_path
        Path to the repository

    output_dir
        Directory to save the output
    """
    map_api = CartographyAPI()
    contents = map_api.search_code_from_directory(repo_path)

    if len(contents) > 0:
        for item in range(len(contents)):
            with open(contents[item]["path"], "r", encoding="utf-8") as f:
                file_content = ast.parse(f.read())

            map_api.visit(file_content)
            map_api.plot_api(output_png=os.path.join(output_dir, str(item) + "api.png"))


@tool
def map_git_history_tool(repo_path: str, output_dir: str = output_dir) -> None:
    """
    Map and visualize the git history of a local repository.

    Parameters
    ----------
    repo_path
        Path to the local repository

    output_dir
        Directory to save the output
    """
    repo = GitHistory()
    git_history = repo.git_history_from_local(path=repo_path, n_commits=20)
    repo.plot_history(git_history, os.path.join(output_dir, "git_history.png"))
