# This file is part of convertdate.
# http://github.com/fitnr/convertdate

# Licensed under the MIT license:
# http://opensource.org/licenses/MIT
# Copyright (c) 2016, fitnr <fitnr@fakeisthenewreal>

.PHONY: all htmlcov test pylint cov format publish build clean

all:

htmlcov: | test
	python -m coverage html

test:
	python -m unittest

pylint:
	pylint src/convertdate

cov:
	python -m coverage run --branch --source=convertdate -m unittest
	python -m coverage report

format:
	black src/ tests/
	isort src/convertdate/*.py src/convertdate/data/*.py tests/*.py

publish: | build
	twine upload dist/*

build: | clean
	python -m build

clean:
	rm -rf build dist
