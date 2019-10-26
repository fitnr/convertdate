# This file is part of convertdate.
# http://github.com/fitnr/convertdate

# Licensed under the MIT license:
# http://opensource.org/licenses/MIT
# Copyright (c) 2016, fitnr <fitnr@fakeisthenewreal>

test:
	coverage run --source convertdate setup.py test
	coverage report
	coverage html

deploy: README.rst
	git push; git push --tags
	rm -rf dist build
	python setup.py sdist bdist_wheel --universal
	twine upload dist/*
