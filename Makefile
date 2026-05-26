.PHONY: clean format test all install

install:
	uv sync --all-groups

clean:
	uv run pyclean . --debris mypy --erase .pdb/**/* .pdb/ obsolete/**/* obsolete/ --yes

format:
	uv run ruff check --select I --fix
	uv run ruff format


test:
	uv run pytest --cov=ramachandraw --cov-report html
