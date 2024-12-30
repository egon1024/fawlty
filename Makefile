MKDOCS_STYLE=readthedocs

# For local documentation authoring
.PHONY: local-docs
local-docs:
	poetry run mkdocs serve -t ${MKDOCS_STYLE} -a 0.0.0.0:8000

# Build and deploy documentation
.PHONY: deploy-docs
deploy-docs:
	poetry run mkdocs gh-deploy -t ${MKDOCS_STYLE}

# Lint the code
.PHONY: lint
lint:
	poetry run flake8 .
	poetry run pylint fawlty