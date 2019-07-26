clean-pyc:
	find . -name '*.pyc' -exec rm --force {} \;; find . -name '*.pyo' -exec rm --force {} \;;

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

test:
	coverage run --source=onemsdk -m unittest discover -v tests && coverage report 

