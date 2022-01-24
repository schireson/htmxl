.PHONY: install format bump lint test build

install:
	poetry install -E beautifulsoup -E lxml

format:
	isort --recursive --quiet src tests
	black src tests

bump:
	bumpversion patch

lint:
	isort --recursive --quiet --check --diff src tests || exit 1
	flake8 src tests || exit 1
	pydocstyle src tests || exit 1
	black --check --diff src tests || exit 1

test:
	coverage run -a -m py.test src tests
	coverage report
	coverage xml
	
publish: build
	poetry publish --build -u __token__ -p '${PYPI_PASSWORD}' --no-interaction
