require python 3.10
conda install -c conda-forge build

python3 -m build

python -m unittest discover -s src -p "*_test.py" -v
python -m unittest discover -s src -p "*_test_integration.py" -v

python -m unittest discover -s src -p "*_test.py" -v && python -m unittest discover -s src -p "*_test_integration.py" -v 

pip install file:////home/abc/Documents/gits/project2/document-structure/dist/document-structure-0.0.0.tar.gz --force-reinstall


remember to install xclip : sudo apt install xclip

