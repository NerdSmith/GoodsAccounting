flake8
mypy . --explicit-package-bases
ruff check . --fix
ruff format .