flake8
mypy . --explicit-package-bases
ruff check .
ruff format .