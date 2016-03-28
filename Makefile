# This file is part of convertdate.
# http://github.com/fitnr/convertdate

# Licensed under the GPL-v3.0 license:
# http://opensource.org/licenses/MIT
# Copyright (c) 2016, fitnr <fitnr@fakeisthenewreal>
test:
	coverage run --include='convertdate/*' setup.py test
	coverage report
	coverage html

deploy: README.rst
	python setup.py register
	git push; git push --tags
	rm -rf dist build
	python3 setup.py bdist_wheel --universal
	twine upload dist/*
