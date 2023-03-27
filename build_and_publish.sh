python setup.py sdist bdist_wheel
twine upload dist/* --verbose
rm -rf dist
rm -rf build
rm -rf *.egg-info