default: dist

dist: clean
	python3 -m build

publish:
	python3 -m twine upload dist/*

clean:
	rm -rf dist *.egg-info
