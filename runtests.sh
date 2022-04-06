#!/bin/bash

for script in tests/*.pyx
do
	echo "Testing with '${script}' as input ..."
	coverage run uncythonize.py ${script} || exit 1
	pyflakes ${script}.py || exit 1
done
