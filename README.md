require python 3.10

remember to install xclip : sudo apt install xclip


## Installation dev env:
- install conda
- create a conda env for this project with python 3.10
  - `conda create --name p6env python=3.10`
- install requirements.txt
  - `conda install --file requirements.txt`
- sometimes, conda bug out, and refuses to install grpcio, so, run this to install grpcio manually
  - `conda install grpcio`
- Test commands:
  - `python -m unittest discover -s src -p "*_test.py" -v`
  - `python -m unittest discover -s src -p "*_test_integration.py" -v`
  - `python -m unittest discover -s src -p "*_test.py" -v && python -m unittest discover -s src -p "*_test_integration.py" -v` 


## Build
- install conda build 
  - `conda install -c conda-forge build`
- build:
  - `python3 -m build`
- built files are in /dist inside this project
- install built file:
  - `pip install dist/document-structure-0.0.0.tar.gz --force-reinstall`


## How to use as an end user?
