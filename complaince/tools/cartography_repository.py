"""Build and plot the tree structure of a repository. """

import os
from collections import defaultdict
from typing import Any

import matplotlib.pyplot as plt
from dotenv import load_dotenv
from github import Auth, Github

load_dotenv()


class CartographyRepo:
    """Build and plot the tree structure of a repository."""

    def __init__(self, removed_files: list[str] = []):
        self.tree: list[str] = []
        self.spec_files = [".git", ".pytest_cache", ".mypy_cache", "__pycache__"] + removed_files

    def build_tree(self, lst_tree: list[str], prefix: str = "") -> None:
        """
        Build the directory tree from a list of paths.

        Parameters
        ----------
        directory
            The directory to build the tree from

        prefix
            The prefix to add to the directory tree

        Examples
        --------
        >>> from complaince.tools.cartography_repository import CartographyRepo
        >>> lst_tree = ['.github/workflows/pkgdown.yaml', '.gitignore']
        >>> tree = CartographyRepo()
        >>> tree.build_tree(lst_tree)
        """
        tree: Any = defaultdict(dict)

        for path in lst_tree:
            parts = path.split('/')
            node = tree
            for part in parts[:-1]:
                node = node.setdefault(part, {})
            node[parts[-1]] = None

        self._generate_tree_from_dict(tree, prefix)

    def _generate_tree_from_dict(self, tree: dict[str, Any], prefix: str = "") -> None:
        """Generate the tree from a dictionary.

        Parameters
        ----------
        tree
            The tree to generate

        prefix
            The prefix to add to the directory tree
        """
        items = list(tree.keys())
        for i, key in enumerate(items):
            connector = '└── ' if i == len(items) - 1 else '├── '
            self.tree.append(prefix + connector + key)
            if isinstance(tree[key], dict):
                extension = '    ' if i == len(items) - 1 else '│   '
                self._generate_tree_from_dict(tree[key], prefix + extension)

    def build_tree_from_directory(self, directory: str = ".", prefix: str = "") -> None:
        """
        Build the directory tree.

        Parameters
        ----------
        directory
            The directory to build the tree from

        prefix
            The prefix to add to the directory tree

        Examples
        --------
        >>> from complaince.tools.cartography_repository import CartographyRepo
        >>> tree = CartographyRepo(removed_files = ["site"])
        >>> tree.build_tree_from_directory()
        """
        entries = sorted(os.listdir(directory))

        for i, entry in enumerate(entries):
            path = os.path.join(directory, entry)

            if entry in self.spec_files:
                continue

            connector = '└── ' if i == len(entries) - 1 else '├── '
            self.tree.append(prefix + connector + entry)

            if os.path.isdir(path):
                extension = '    ' if i == len(entries) - 1 else '│   '
                self.build_tree_from_directory(path, prefix + extension)

    def build_tree_from_github(self, repo_name: str) -> list[str]:
        """
        Build the directory tree from a Github repository.

        Parameters
        ----------
        repo
            The Github repository

        Examples
        --------
        >>> from complaince.tools.cartography_repository import CartographyRepo
        >>> tree = CartographyRepo(removed_files = ["pkgdown"])
        >>> lst_tree = tree.build_tree_from_github("alexym1/booklet")
        >>> tree.build_tree(lst_tree)
        """

        def list_paths(repo: Any, path: str = "", removed_files: list[str] = self.spec_files) -> list[str]:
            """
            List all paths in a repository.

            Parameters
            ----------
            repo
                The Github repository

            path
                The path to list

            removed_files
                The list of files to remove

            Returns
            -------
            The list of paths
            """
            contents = repo.get_contents(path)
            all_paths = []
            for content in contents:
                full_path = content.path
                if content.type == "dir" and full_path not in removed_files:
                    all_paths.append(full_path + "/")
                    all_paths.extend(list_paths(repo, full_path))
                else:
                    all_paths.append(full_path)
            return all_paths

        if os.getenv("GITHUB_TOKEN") is None:
            github = Github()
        else:
            auth = Auth.Token(str(os.getenv("GITHUB_TOKEN")))
            github = Github(auth=auth)

        repo = github.get_repo(repo_name)
        lst_tree = list_paths(repo)

        return lst_tree

    def display_tree(self) -> str:
        """Display the repository tree."""
        return "\n".join(self.tree)

    def plot(self, output_png: str) -> None:
        """Plot the repository tree.

        Parameters
        ----------
        output_png
            The output png file to save the plot

        Examples
        --------
        >>> import os
        >>> from tempfile import TemporaryDirectory
        >>> from complaince.tools.cartography_repository import CartographyRepo

        >>> temp_dir = TemporaryDirectory(prefix="treemap_")
        >>> tree = CartographyRepo(removed_files = ["site"])
        >>> tree.build_tree_from_directory()
        >>> tree.plot(output_png = os.path.join(temp_dir.name, "treemap.png"))
        """
        tree_text = self.display_tree()

        _, ax = plt.subplots(figsize=(8, len(self.tree) * 0.3))
        ax.text(0.01, 1, tree_text, fontsize=12, family="monospace", verticalalignment="top")

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        plt.title("Tree Structure of the Repository", fontsize=14)
        plt.savefig(output_png)


if __name__ == "__main__":
    import argparse
    import logging

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Generate a repository tree map.")
    parser.add_argument("directory", nargs="?", default=".", help="Path to the repository (default: current directory)")
    parser.add_argument("--remove", nargs="*", default=[], help="List of files or directories to remove from the tree")
    args = parser.parse_args()

    tree = CartographyRepo(removed_files=args.remove)
    tree.build_tree_from_directory(args.directory)
    logging.info(tree.display_tree())
