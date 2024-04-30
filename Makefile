setup: install just-build package-force-reinstall

setup-linux: install just-build package-force-reinstall-linux

install:
	poetry install

just-build:
	poetry build

test:
	poetry run pytest -vv

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

package-install:
	python -m pip install --user dist/*.whl

remove-envs:
	rm -rf .venv && poetry env remove --all

package-force-reinstall:
	python -m pip install --user --force-reinstall dist/*.whl

package-force-reinstall-linux:
	python3 -m pip install --user --force-reinstall dist/*.whl