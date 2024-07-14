.PHONY: clean format test all

clean:
	pyclean . --debris mypy --erase .pdb/**/* .pdb/ obsolete/**/* obsolete/ --yes

format:
	ruff format ramachandraw/ tests/ scripts/

test:
	pytest --cov=ramachandraw --cov-report html

all: clean format test
