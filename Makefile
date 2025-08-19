# test to ensure tab is not spaces
_test:
	@echo "success"

style:
	black .
	isort . --profile=black

lint:
	pylint --rcfile=pylintrc.conf $$(git ls-files '*.py')

lint+: style lint

test:
	pytest .