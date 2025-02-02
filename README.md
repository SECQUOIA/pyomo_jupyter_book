# pyomo_jupyter_book
A conversion of the Pyomo workshop into a jupyter book

Find the companion website [here](https://secquoia.github.io/pyomo_jupyter_book/intro.html)


### How to build locally
Ensure you've opened the directory of the jupyter-book as the working directory. You should have a _config.yml and _toc.yml file in this directory. Make sure you're in a virtual environment. Install jupyter-book is using:
`pip install jupyter-book`
then
`jupyter-book build ./`
to build the current working directory into a jupyter-book.

The html is in the folder `_build\html\` and you can preview the book by opening the file `_build\html\index.html` in your browser, using VSCode's preview functionality (recommended), or running a the file via a browser executable in command line.

Following this, to deploy your build to the github page, we will be using the `ghp-import` library.

Install using `pip install ghp-import`

Now run `ghp-import -n -p -f -b BRANCHNAME _build/html`

**NOTE: This is a destructive action. It will overwrite any branch named BRANCHNAME and assume it is 100% derivative**

The -b tag should be followed by the branch which you wish to deploy the html to. By default it is gh-pages. If you're wishing to non-destructively test a local build, push to a separate branch name, and change the branch referenced for the github page in the settings, allowing for a quick revert to the gh-pages branch.

The -n tag indicates building without Jekyll

The -p and -f tags indicate force pushing this branch after committing it.
