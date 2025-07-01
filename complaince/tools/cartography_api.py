"""Cartography the API."""

import ast
import os
from collections import defaultdict
from typing import Any

import matplotlib.pyplot as plt
from dotenv import load_dotenv
from github import Auth, Github
from github.Repository import Repository

load_dotenv()


class CartographyAPI(ast.NodeVisitor):
    """Cartography the API."""

    def __init__(self):
        self.call_tree = defaultdict(lambda: defaultdict(dict))
        self.current_function = None
        self.function_defs = {}
        self.http_methods = {}
        self.endpoints = {}

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definitions and store their body.

        Parameters
        ----------
        node
            The AST node to visit
        """
        self.function_defs[node.name] = node
        self.current_function = node.name

        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                if decorator.func.attr in {"get", "post", "put", "delete", "patch"}:
                    self.http_methods[node.name] = decorator.func.attr
                    if decorator.args:
                        path = ast.literal_eval(decorator.args[0])
                        self.endpoints[node.name] = path

        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node: ast.Call) -> None:
        """Capture function calls and map them to the caller.

        Parameters
        ----------
        node
            The AST node to visit
        """
        if isinstance(node.func, ast.Name):
            called_function = node.func.id

        if isinstance(node.func, ast.Attribute):
            called_function = node.func.attr

        if self.current_function:
            self.call_tree[self.current_function][called_function] = {}

        self.generic_visit(node)

    def resolve_hierarchy(self) -> None | dict:
        """Recursively build a function call hierarchy with HTTP method types."""

        def resolve(func_name, tree: dict[str, Any], visited: set[str]) -> None:
            """Recursively resolve the function call hierarchy.

            Parameters
            ----------
            func_name
                The function name to resolve

            tree
                The tree structure to build

            visited
                The set of visited functions
            """
            if func_name in visited:
                return None

            visited.add(func_name)

            if func_name in self.call_tree:
                for called_func in self.call_tree[func_name]:
                    tree[called_func] = {}
                    resolve(called_func, tree[called_func], visited)

        root_tree = {}
        for func, method in self.http_methods.items():
            endpoint = self.endpoints.get(func, f"/{func}/")
            root_tree[endpoint] = {"method": method.upper(), "functions": {}}
            resolve(func, root_tree[endpoint]["functions"], set())
        return root_tree

    def search_code_from_directory(self, dir_path: str = "", path: str = "") -> list[dict[str, str]]:
        """
        Search for FastAPI code in a local repository.

        Parameters
        ----------
        dir_path
            The repository to search

        path
            The path to search

        Returns
        -------
        A list of files containing "FastAPI" code
        """
        results = []
        for root, _, files in os.walk(os.path.join(os.getcwd(), dir_path, path)):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            file_content = f.read()
                            if "FastAPI" in file_content:
                                results.append({"path": file_path, "url": "", "snippet": file_content})
                    except Exception:
                        pass

        return results

    def get_api_from_github(self, repo_name: str) -> list[dict[str, str]]:
        """
        Get the FastAPI code from a GitHub repository.

        Parameters
        ----------
        repo_name
            The repository name

        Returns
        -------
        A list of dictionaries containing the path, url and snippet of the code

        Examples
        --------
        >>> import ast
        >>> from complaince.tools.cartography_api import CartographyAPI

        >>> mapper = CartographyAPI()
        >>> contents = mapper.get_api_from_github("marciovrl/fastapi")
        >>> tree = ast.parse(contents[0]["snippet"])
        >>> mapper.visit(tree)
        >>> tree_string = mapper.tree_as_string()
        """
        if os.getenv("GITHUB_TOKEN") is None:
            github = Github()
        else:
            auth = Auth.Token(str(os.getenv("GITHUB_TOKEN")))
            github = Github(auth=auth)

        repo = github.get_repo(repo_name)
        contents = search_code_from_github(repo)

        return contents

    def tree_as_string(self, tree: None | dict[str, dict[str, Any]] = None, prefix: str = "") -> str:
        """Convert the tree structure to a string representation.

        Parameters
        ----------
        tree
            The tree structure to convert

        prefix
            The prefix to add to each line

        Returns
        -------
        The tree structure as a list of strings

        Examples
        --------
        >>> import ast
        >>> from complaince.tools.cartography_api import CartographyAPI

        >>> with open("./data/fake_repo/fastapi_web_app.py", "r", encoding="utf-8") as f:
        ...    tree = ast.parse(f.read())

        >>> mapper = CartographyAPI()
        >>> mapper.visit(tree)
        >>> tree_string = mapper.tree_as_string()
        """
        if tree is None:
            new_tree = self.resolve_hierarchy()

        if new_tree is None:
            return ""

        lines = []
        for _, (key, value) in enumerate(new_tree.items()):
            lines.append(f"{prefix}{key} ({value['method']})")
            new_prefix = prefix + ('    ')

            for _, (func_name, _) in enumerate(value["functions"].items()):
                if func_name not in {"get", "post", "put", "delete", "patch"}:
                    lines.append(f"{new_prefix}└── {func_name}()")
                    new_prefix += "    "

            lines.append(f"{new_prefix}└── output")

        return "\n".join(lines)

    def plot_api(self, output_png: str = "api.png") -> None:
        """Plot the tree structure using matplotlib.

        Parameters
        ----------
        output_png
            The output png file to save the plot

        Examples
        --------
        >>> import os
        >>> import ast
        >>> from tempfile import TemporaryDirectory
        >>> from complaince.tools.cartography_api import CartographyAPI

        >>> with open("./data/fake_repo/fastapi_web_app.py", "r", encoding="utf-8") as f:
        ...    tree = ast.parse(f.read())

        >>> temp_dir = TemporaryDirectory(prefix="api_")

        >>> mapper = CartographyAPI()
        >>> mapper.visit(tree)
        >>> mapper.plot_api(os.path.join(temp_dir.name, "api.png"))
        """
        tree = self.resolve_hierarchy()

        if tree is not None:
            tree_text = self.tree_as_string()

            _, ax = plt.subplots(figsize=(8, len(tree) * 2))
            ax.text(0.01, 1, tree_text, fontsize=12, family="monospace", verticalalignment="top")

            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis("off")

            plt.title("API Tree Structure")
            plt.savefig(output_png)


def search_code_from_github(repo: Repository, path: str = "") -> list[dict[str, str]]:
    """
    Search for FastAPI code in a repository.

    Parameters
    ----------
    repo
        The repository to search

    path
        The path to search

    Returns
    -------
    A list of dictionaries containing the path, url and snippet of the code
    """
    results = []
    contents = repo.get_contents(path)

    if isinstance(contents, list):
        for content_file in contents:
            if content_file.type == "dir":
                results += search_code_from_github(repo, content_file.path)
            elif content_file.type == "file" and content_file.name.endswith(".py"):
                try:
                    file_content = content_file.decoded_content.decode("utf-8")
                    if "FastAPI" in file_content:
                        results.append(
                            {"path": content_file.path, "url": content_file.html_url, "snippet": file_content}
                        )
                except Exception:
                    pass
    return results


if __name__ == "__main__":
    import argparse
    import logging

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Generate an API tree map.")
    parser.add_argument("directory", nargs="?", default=".", help="Path to the API file")
    args = parser.parse_args()

    with open(args.directory, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    mapper = CartographyAPI()
    mapper.visit(tree)
    tree_string = mapper.tree_as_string()
    logging.info(tree_string)
