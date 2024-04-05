setup: install just-build package-force-reinstall

just-build:
	poetry build

install:
	poetry install

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml

test-coverage-simple:
	poetry run pytest --cov-report term-missing --cov=gendiff

lint:
	poetry run flake8 gendiff

selfcheck:
	poetry check

check: selfcheck test lint

build: check
	poetry build

.PHONY: install test lint selfcheck check build

package-install:
	python -m pip install --user dist/*.whl


package-force-reinstall:
	python -m pip install --user --force-reinstall dist/*.whl
