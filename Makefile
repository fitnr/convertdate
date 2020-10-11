# This file is part of convertdate.
# http://github.com/fitnr/convertdate

# Licensed under the MIT license:
# http://opensource.org/licenses/MIT
# Copyright (c) 2016, fitnr <fitnr@fakeisthenewreal>

.PHONY: all htmlcov test deploy format
all:

htmlcov: | test
	python -m coverage html

cov:
	python -m coverage run --branch --source=convertdate -m unittest
	python -m coverage report

format:
	black src/ tests/
	isort src/convertdate/*.py src/convertdate/data/*.py tests/*.py

deploy:
	rm -rf dist build
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*
	git push; git push --tags
