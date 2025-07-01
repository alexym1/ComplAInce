# Contributing

## Get Started

1. Clone the repository

```shell
git clone https://github.com/alexym1/ComplAInce.git
```

2. Create a branch (from the master branch)

```shell
git checkout -b branch_name
```

3. Install package

```shell
make init
make install-prod
```

4. Making changes, and check your work:

```shell
make preco
make unittest
make test-docstrings
```

5. Commit

```shell
git add .
git commit -m "your message"
```

6. Push your branch

```shell
git push origin branch_name
```


## Create a pull request

1. `make preco`

2. `make unittest`

3. `make bump2version XXXXX` (choices : major / minor / patch)

4. Update CHANGELOG.md with new entry

5. Generate the docs using `make docs`

6. Create a PR from to master

7. Review the PR and merge it.
