sudo pip install -U mistune

# Run the Jupyter notebook
jupyter nbconvert --ExecutePreprocessor.timeout=600 --to python nb.ipynb

# Generate HTML output
jupyter-nbconvert --execute ""
