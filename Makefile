# test to ensure tab is not spaces
_test:
	@echo "success"

format:
	isort .

lint:
	pylint --rcfile=pylintrc.conf $$(git ls-files '*.py')

lint+: format lint