require python 3.10

python3 -m build

python -m unittest discover -s src -p "*_test.py" -v

pip install file:///abc/document-structure-0.0.0.tar.gz --force-reinstall

