# pyomo_jupyter_book
A conversion of the Pyomo workshop into a jupyter book

Find the companion website [here](https://secquoia.github.io/pyomo_jupyter_book/intro.html)


### How to build locally
Ensure you've opened the directory of the jupyter-book as the working directory. You should have a _config.yml and _toc.yml file in this directory. Make sure you're in a virtual environment. Install jupyter-book is using:
`pip install jupyter-book`
then
`jupyter-book build ./`
to build the current working directory into a jupyter-book.

The html is in the folder `_build\html\` and you can preview the book by opening the file `_build\html\index.html`