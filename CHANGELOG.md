# Changelog

## 1.1.0 - (2025-08-02)

Related PR: (#7)

Here we would have the update steps for 1.1.0 for people to follow.

### Added

- Main files to run AI agent (#4):
    - Add `complaince_api.py` file related to API
    - Add `Dockerfile` & `docker.sh`
    - Add `monitoring.py` to record messages of LLM

- Add basick prompt example to run the AI agent

### Modified

- `Contributing.md` and `PULL_REQUEST_TEMPLATE.md` have been updated to generate online documentation (#3)
- Harmonize title of `cartography_*` files

### Fixed

- `make docs` renders the online documentation (#5)


## 1.0.0 - (2025-07-01)

Related PR: (#2)

Here we would have the update steps for 1.0.0 for people to follow.

### Added

- Main tools to make code remediation including:
    - `cartography_api.py`
    - `cartography_history.py`
    - `cartography_repository.py`

- Fake repository in `data` folder
- Unit tests related to `cartography_*.py`
- Handle deps using `poetry`
- Documentation using `mkdocs`
