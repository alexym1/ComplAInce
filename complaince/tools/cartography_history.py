"""Git history of repository."""

import os

import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv
from git import Repo
from github import Auth, Github

load_dotenv()


class GitHistory:
    """Build and plot the git history of a repository."""

    def __init__(self, removed_branches: list[str] = []):
        self.removed_branches = ["gh-pages"] + removed_branches

    def git_history_from_local(self, path: str = ".", n_commits: int = 20) -> pd.DataFrame:
        """
        Fetch the history of a local repository.

        Parameters
        ----------
        path
            Path to the local repository

        n_commits
            Number of commits to fetch

        Returns
        -------
        DataFrame containing the history of the repository.

        Examples
        --------
        >>> from complaince.tools.cartography_history import GitHistory
        >>> repo = GitHistory()
        >>> df = repo.git_history_from_local(n_commits=10)
        """
        repo = Repo(path)

        commit_data = []
        for branch in repo.branches:
            if branch not in self.removed_branches:
                commits = list(repo.iter_commits(branch, max_count=n_commits))

                for commit in commits:
                    sha = commit.hexsha[:7]
                    author = commit.author.name
                    date = commit.committed_datetime.strftime("%Y-%m-%d %H:%M")
                    message = commit.message.strip()
                    commit_data.append([message, date, author, sha, branch])

        history = pd.DataFrame(commit_data, columns=["Description", "Date", "Author", "Commit", "Branch"])
        ordered_history = history.sort_values("Date", ascending=False).reset_index(drop=True)
        git_history = ordered_history.iloc[:n_commits, :]

        return git_history

    def git_history_from_github(self, repo_name: str, n_commits: int = 20) -> pd.DataFrame:
        """
        Fetch the history of a GitHub repository.

        Parameters
        ----------
        repo_name
            Full name of the repository in the format "owner/repo"

        n_commits
            Number of commits to fetch

        Returns
        -------
        DataFrame containing the history of the repository.

        Examples
        --------
        >>> from complaince.tools.cartography_history import GitHistory
        >>> repo = GitHistory()
        >>> history = repo.git_history_from_github("alexym1/booklet", n_commits=20)
        """
        if os.getenv("GITHUB_TOKEN") is None:
            github = Github()
        else:
            auth = Auth.Token(str(os.getenv("GITHUB_TOKEN")))
            github = Github(auth=auth)

        repo = github.get_repo(repo_name)
        branches = list(repo.get_branches())

        commit_data = []
        for branch in branches:
            if branch.name not in self.removed_branches:
                commits = list(repo.get_commits(sha=branch.name))[:n_commits]

                for commit in commits:
                    sha = commit.sha[:7]
                    author = commit.commit.author.name
                    date = commit.commit.committer.date.strftime("%Y-%m-%d %H:%M")
                    description = commit.commit.message.split("\n")[0]
                    branch_name = branch.name
                    commit_data.append([description, date, author, sha, branch_name])

        history = pd.DataFrame(commit_data, columns=["Description", "Date", "Author", "Commit", "Branch"])
        ordered_history = history.sort_values("Date", ascending=False).reset_index(drop=True)
        git_history = ordered_history.iloc[:n_commits, :]

        return git_history

    def plot_history(self, history: pd.DataFrame, output_png: str) -> None:
        """
        Plot the history of a repository.

        Parameters
        ----------
        history
            DataFrame containing the history of the repository

        output_png
            Path to save the plot

        Examples
        --------
        >>> import os
        >>> from tempfile import TemporaryDirectory
        >>> from complaince.tools.cartography_history import GitHistory

        >>> temp_dir = TemporaryDirectory(prefix="history_")
        >>> repo = GitHistory()
        >>> git = repo.git_history_from_local(n_commits=10)
        >>> repo.plot_history(git, output_png = os.path.join(temp_dir.name, "history.png"))
        """
        branch_positions = {branch: i for i, branch in enumerate(history["Branch"].unique())}
        history["y"] = history["Branch"].map(branch_positions)

        _, ax = plt.subplots(figsize=(15, 10))

        for _, row in history.iterrows():
            ax.scatter(row["Date"], row["y"], s=100, label=row["Branch"], edgecolors="black", zorder=2)
            ax.text(row["Date"], row["y"] + 0.15, row["Commit"], ha="center", fontsize=9, color="black")

        for i in range(len(history) - 1):
            ax.plot(
                [history.iloc[i]["Date"], history.iloc[i + 1]["Date"]],
                [history.iloc[i]["y"], history.iloc[i + 1]["y"]],
                color="gray",
                linestyle="-",
                alpha=0.6,
                zorder=1,
            )

        history.drop(columns="y", inplace=True)

        ax.set_yticks(list(branch_positions.values()))
        ax.set_yticklabels(list(branch_positions.keys()))
        ax.set_xlabel("Date")
        ax.grid(axis="x", linestyle="--", alpha=0.5)

        plt.xticks(rotation=45)
        plt.title("Gitflow of the Repository", fontsize=14)
        plt.savefig(output_png)


if __name__ == "__main__":
    import argparse
    import logging

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Return versioning history of the repo.")
    parser.add_argument("directory", nargs="?", default=".", help="Path to the repository (default: current directory)")
    parser.add_argument("-n", type=int, default=10, help="Number of commits to fetch")
    args = parser.parse_args()

    repo = GitHistory()
    df = repo.git_history_from_local(path=args.directory, n_commits=args.n)
    logging.info(df)
