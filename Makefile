# This file is part of convertdate.
# http://github.com/fitnr/convertdate

# Licensed under the MIT license:
# http://opensource.org/licenses/MIT
# Copyright (c) 2016, fitnr <fitnr@fakeisthenewreal>

.PHONY: all htmlcov test deploy
all:

htmlcov: | test
	python -m coverage html

test:
	python -m coverage run --branch --source=convertdate -m unittest discover -s tests
	python -m coverage report

deploy:
	rm -rf dist build
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*
	git push; git push --tags
