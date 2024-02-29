.PHONY: clean format test all

clean:
	pyclean .
	rm -rf .pdb/ obsolete/ .mypy_cache/ .pytest_cache/ .ruff_cache/ htmlcov/ .coverage

format:
	ruff format ramachandraw/ tests/ scripts/
	ruff --fix ramachandraw/ tests/ scripts/

test:
	pytest --cov=ramachandraw --cov-report html

all: clean format test
