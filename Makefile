.PHONY: clean
clean:
	rm -r build dist vedro_lazy_rerunner.egg-info .mypy_cache .pytest_cache

.PHONY: install
install:
	pip3 install --quiet -r requirements.txt -r requirements-dev.txt

.PHONY: install-vedro-lazy-rerunner
install-vedro-lazy-rerunner:
	python3 setup.py install

.PHONY: check-types
check-types:
	python3 -m mypy vedro_lazy_rerunner --strict

.PHONY: check-imports
check-imports:
	python3 -m isort --check-only .

.PHONY: sort-imports
sort-imports:
	python3 -m isort .

.PHONY: check-style
check-style:
	python3 -m flake8 .

.PHONY: lint
lint: check-types check-style check-imports

.PHONY: test
test:
	python3 -m pytest
