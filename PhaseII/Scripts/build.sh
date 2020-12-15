#!/bin/bash

conda activate pyvizenv


## Run the Jupyter notebook
jupyter nbconvert --ExecutePreprocessor.timeout=600 --to python nb.ipynb


"01_Pre_Processing/01_AnonymizeData.ipynb"



## Generate HTML output
jupyter-nbconvert --execute ""
