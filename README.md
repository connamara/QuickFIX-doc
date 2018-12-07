# QuickFIX-doc
[![Build Status](https://travis-ci.org/connamara/QuickFIX-doc.svg?branch=master)](https://travis-ci.org/connamara/QuickFIX-doc)

QuickFIX-doc parses QuickFIX data dictionary .xml files into descriptive [reStructuredText](http://docutils.sourceforge.net/rst.html) files using [RstCloth](https://pypi.org/project/rstcloth/), and then runs them through the [Sphinx](http://www.sphinx-doc.org/) documentation generation library for Python.

## Usage
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

## Install
1) Ensure Python is installed on your machine - [see here](https://wiki.python.org/moin/BeginnersGuide/Download)
2) Clone this repository to a local folder
3) `cd` into the folder and run `pip install .`

## Tests
1) Ensure [Docker](https://www.docker.com/get-started) is installed on your machine
2) Execute `./acceptance.sh`
3) Detailed reports will be available for each vanilla FIX spec under `./acceptance/FIX*`
    * Each subdirectory includes [Robot Framework](http://robotframework.org/) report files
    * `log.html`, `report.html`, and `output.xml`

## Background and Goals
Writing specs for FIX **sucks**. QuickFIX-doc helps you "save time and look good" by taking care of the specification generation for you.

All you need is a valid QuickFIX data dictionary. No need for any custom word documents, no chance for human error, just run and view your nice beautiful spec.

## Contributing
Please see the [contribution guidelines](CONTRIBUTION_GUIDELINES.md)

## Credits
Contributers:

* [Mike Wilner](https://github.com/michaelwilner)
* [Chris Busbey](https://github.com/cbusbey)

![Connamara Systems](http://www.connamara.com/wp-content/uploads/2016/01/connamara_logo_dark.png)

QuickFIX-doc is maintained and funded by [Connamara Systems, llc](http://connamara.com).

The names and logos for Connamara Systems are trademarks of Connamara Systems, llc.

## Licensing
QuickFIX-doc is Copyright © 2018 Connamara Systems, llc.

This software is available under the GPL and a commercial license.  Please see the [LICENSE](LICENSE) file for the terms specified by the GPL license.  The commercial license offers more flexible licensing terms compared to the GPL, and includes support services.  [Contact us](mailto:info@connamara.com) for more information on the Connamara commercial license, what it enables, and how you can start commercial development with it.

This product includes software developed by quickfixengine.org ([http://www.quickfixengine.org/](http://www.quickfixengine.org/)). Please see the [QuickFIX Software LICENSE](QUICKFIX_LICENSE) for the terms specified by the QuickFIX Software License.