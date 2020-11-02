#!/usr/bin/env python
from setuptools import setup


setup(
    name='QuickFIX-doc',
    version='0.7',
    description='QuickFIX data dictionary XML spec documentation generator',
    author='Michael L. Wilner',
    author_email='mwilner@connamara.com',
    packages=['quickfix_doc','quickfix_doc.datadictionary','quickfix_doc.restructuredtext'],
    install_requires=['pyyaml','sphinx','rstcloth'],
    license='The QuickFIX License',
    include_package_data=True,
    entry_points = {
              'console_scripts': [
                  'quickfixdoc=quickfix_doc.__main__:main',
              ],
          },
    zip_safe=False
)
