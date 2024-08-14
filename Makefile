# test to ensure tab is not spaces
_test:
	@echo "success"

format:
	black .
	isort . --profile=black

lint:
	pylint --rcfile=pylintrc.conf $$(git ls-files '*.py')

lint+: format lint