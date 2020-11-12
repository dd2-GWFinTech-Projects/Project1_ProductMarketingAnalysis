
conda activate pyvizenv

# Install date parsing library 'dateparser'
pip install dateparser

# Install time duration parsing (https://pypi.org/project/pytimeparse/)
pip install pytimeparse

# Install toolchain to run Jupyter notebook from command line
sudo pip install -U mistune
## Run the Jupyter notebook
jupyter nbconvert --ExecutePreprocessor.timeout=600 --to python nb.ipynb
## Generate HTML output
jupyter-nbconvert --execute ""
