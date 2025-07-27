# ComplAInce

> An AI agent to speed up code remediation

## Overview

ComplAInce is a suite of tools and an AI agent designed to simplify understanding a code repository. It includes features to map out the folder structure, source code, and Git history.

Imagine this: you inherit an IT project burdened with massive technical debt — no coding best practices, files with no structure or logic. The whole thing is 99.99999% vibe-coded. That’s where ComplAInce comes in! Why bother manually navigating through the project tree when an AI agent can do it for you? 

👉 Reduce cognitive complexity
👉 Simplified code remediation
👉 Easy way to spot bugs


## Installation

```shell
pip install -U complaince
```

## Key Features

| Feature          | Local     | Github    | Gitlab    | Bitbucket |
|------------------|-----------|-----------|-----------|-----------|
| Cartography repo | ✅        | ✅        | ❌        | ❌       |
| Fetch git history| ✅        | ✅        | ❌        | ❌       |
| Cartography API* | ✅        | ✅        | ❌        | ❌       |


*Only FastAPI is considered*


## Example

### Set up ENV variable

```bash
GITHUB_TOKEN=<YOUR_GITHUB_TOKEN>
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
```

### ComplAInce as SDK

Compliance components can be used as building blocks, eliminating the need to call a LLM.

```python
from complaince.tools.cartography_repository import CartographyRepo
tree = CartographyRepo(removed_files = ["site"])
tree.build_tree_from_directory(".")
print(tree.display_tree())
```

OR

```shell
python complaince/tools/cartography_repository.py --remove site docs dist
python complaince/tools/cartography_api.py data/fake_repo/fastapi_web_app.py
python complaince/tools/cartography_history.py -n 20
```

### ComplAInce as API

Run the AI agent.

```shell
uvicorn complaince.exposition:complaince_api --host 0.0.0.0
```

OR

```python
import uvicorn
uvicorn.run("complaince.exposition:complaince_api:app", host="0.0.0.0", port=8000)
```

OR

```shell
make docker-build
make docker-run
```

Then, open http://127.0.0.1:8000/docs#/default/ and run the API.


## Code of conduct

Please note that this project is released with a [Contributor Code of
Conduct](https://github.com/alexym1/ComplAInce/blob/master/CONTRIBUTING.md). By
participating in this project you agree to abide by its terms.
