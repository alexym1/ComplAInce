# ComplAInce

> A better way to speed up code remediation

## Overview

Code remediation was frequently necessary to scale algorithms from proof of concept (POC) to production. However, a considerable amount of time was often required to understand the repository’s purpose, architecture, and key components before any substantive modifications could be made. Consequently, less time was available for implementing new features or addressing bugs, ultimately slowing the overall development process.

To address this challenge, ComplAInce was developed to streamline the extraction of key components from a codebase. It accelerates the remediation process by significantly reducing the time needed for manual exploration and comprehension of the repository.


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
GITHUB_TOKEN=YOUR_GITHUB_TOKEN
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

## Code of conduct

Please note that this project is released with a [Contributor Code of
Conduct](https://github.com/alexym1/ComplAInce/blob/master/CONTRIBUTING.md). By
participating in this project you agree to abide by its terms.
