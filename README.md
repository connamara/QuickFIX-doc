# QuickFIX-doc
#### Author: Michael L. Wilner
#### © 2018 Connamara Systems
Automatic documentation generation for QuickFIX XML Data Dictionaries

## Running
```
quickfixdoc PATH/TO/DD.xml PATH/TO/OUTPUT/DIRECTORY [BUILDER (default: html)]
```

Example:
```
> quickfixdoc ~/Documents/quickfix/spec/FIX44.xml ./FIX_44_Spec/
QuickFIXdoc
Generating documents for ~/Documents/quickfix/spec/FIX44.xml into ./FIX_44_Spec/
Running: /usr/local/opt/python/bin/python3.7 -m sphinx.cmd.build -M html ./FIX_44_Spec/ ./FIX_44_Spec/
Running Sphinx v1.8.1
making output directory...
building [mo]: targets for 0 po files that are out of date
building [html]: targets for 96 source files that are out of date
updating environment: 96 added, 0 changed, 0 removed
reading sources... [100%] index                                                                                                 
looking for now-outdated files... none found
pickling environment... done
checking consistency... done
preparing documents... done
writing output... [100%] index                                                                                                  
generating indices... genindex
writing additional pages... search
copying static files... done
copying extra files... done
dumping search index in English (code: en) ... done
dumping object inventory... done
build succeeded.

The HTML pages are in FIX_44_Spec/html.
```

## Background and Goals
Writing specs for FIX **sucks**. QuickFIX-doc helps you "save time and look good" by taking care of the specification generation for you.

All you need is a valid QuickFIX data dictionary. No need for any custom word documents, no chance for human error, just run and view your nice beautiful spec.

QuickFIX-doc parses the QuickFIX data dictionary .xml files into descriptive [reStructuredText](http://docutils.sourceforge.net/rst.html) files using [RstCloth](https://pypi.org/project/rstcloth/), and then runs them through the [Sphinx](http://www.sphinx-doc.org/) documentation generation library for Python.

## Installing
1) Ensure Python is installed on your machine - [see here](https://wiki.python.org/moin/BeginnersGuide/Download)
2) Clone this repository to a local folder
3) `cd` into the folder and run `pip install .`
