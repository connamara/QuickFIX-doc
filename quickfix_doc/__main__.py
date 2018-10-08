#!/usr/bin/env python

import xml.etree.ElementTree
import os
import sys
import subprocess
from . import datadictionary
from . import restructuredtext


def parse_data_dictionary(data_dict_xml_path, output_path):
    """Produce Sphinx documentation from a QuickFIX data dictionary

    Arguments:
        data_dict_xml_path -- path/to/data_dictionary/FIX.xml
        output_path -- directory to dump data dictionary output
    """
    e = xml.etree.ElementTree.parse(data_dict_xml_path).getroot()
    spec_name, base_file = datadictionary.util.get_doc_title(e.tag, e.attrib, data_dict_xml_path)
    # Get the fields
    flds = next(elem for elem in e if str(elem.tag).lower() == datadictionary.fields.FIELD_TAG+"s")
    parsed_flds = datadictionary.fields.parse_fields(flds)
    # Now get the components ready
    comps = None
    try:
        comps = next(elem for elem in e if str(elem.tag).lower() == datadictionary.components.COMPONENT_TAG + "s")
    except:
        pass
    parsed_comps = datadictionary.components.parse_components(comps) if comps is not None else dict()
    #Finally, go parse messages
    head = None
    try:
        head = next(elem for elem in e if str(elem.tag).lower() == "header")
    except:
        pass
    tail = None
    try:
        tail = next(elem for elem in e if str(elem.tag).lower() == "trailer")
    except:
        pass
    msgs = next(elem for elem in e if str(elem.tag).lower() == datadictionary.messages.MESSAGE_TAG + "s")
    parsed_msgs = datadictionary.messages.parse_messages(msgs, head, tail)
    return restructuredtext.produce_base.make_restructured_text(spec_name, base_file, data_dict_xml_path, output_path, parsed_msgs, parsed_comps, parsed_flds)


def main(args=None):
    print("QuickFIX-doc")
    if args is None:
        args = sys.argv[1:]
    if len(args) < 2:
        print("usage: quickfixdoc PATH/TO/DD.xml PATH/TO/OUTPUT/DIRECTORY [BUILDER (default: html)]")
        sys.exit(1)
    build_path = args[1]
    sphinx_builder = 'html'
    try:
        sphinx_builder = args[2]
    except:
        pass
    print("Generating documents for "+args[0]+ " into "+build_path)
    rst = parse_data_dictionary(data_dict_xml_path=args[0], output_path=build_path)
    for rst_file in rst:
        parent_path = os.path.abspath(os.path.join(rst_file, ".."))
        if not os.path.exists(parent_path):
            os.makedirs(parent_path)
        with open(rst_file, 'w+') as output_file:
            output_file.write(rst[rst_file])
    sphinx_args = [sys.executable, '-m', 'sphinx.cmd.build', '-M', sphinx_builder, build_path, build_path]
    print('Running: '+' '.join(sphinx_args))
    return subprocess.call(sphinx_args)


if __name__ == '__main__':
    sys.exit(main())
