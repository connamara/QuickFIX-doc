import os
from . import components
ROOT_DOCUMENT_TAG = 'fix'


def parse_bool_yn(yn_bool_str):
    """Parse a string representation of a boolean to its python equivalent"""
    val_str = str(yn_bool_str).strip().upper()
    val_first_char = str(val_str[0])
    return True if val_first_char == "Y" or val_first_char == "T" else False


def parse_child_elem(child_elem):
    """Parse Data Dictionary XML Child Elements

    Arguments:
        child_elem -- XML document element for a child element
    """
    child_elem_dict = dict()
    child_elem_dict['type'] = str(child_elem.tag)
    child_elem_dict['required'] = parse_bool_yn(str(child_elem.attrib['required']).strip())
    child_elem_name = str(child_elem.attrib['name']).strip()
    if child_elem_dict['type'] == 'group':
        group_elems_dict = components.parse_component(child_elem)
        comp_elems_dict = [group_elems_dict, child_elem_dict['required']]
        return child_elem_name, comp_elems_dict
    else:
        return child_elem_name, child_elem_dict


def get_doc_title(root_xml_tag, root_xml_attrib, data_dict_xml_path):
    """Generate document title for Sphinx documentation

    Arguments:
        root_xml_tag -- XML document root tag
        root_xml_attrib -- XML document root attributes
        data_dict_xml_path -- os path to the QuickFIX data dictionary
    """
    base_file = os.path.basename(data_dict_xml_path)
    root_tag = str(root_xml_tag).strip()
    if root_tag.lower() != ROOT_DOCUMENT_TAG.lower():
        raise ValueError(root_tag + " document root tag is not equal to " + ROOT_DOCUMENT_TAG)
    version_major = int(root_xml_attrib['major'])
    version_minor = int(root_xml_attrib['minor'])
    spec_name = '.'.join(("FIX", str(version_major), str(version_minor)))
    try:
        version_servicepack = int(root_xml_attrib['servicepack'])
        if version_servicepack != 0:
            spec_name += 'SP'+str(version_servicepack)
    except:
        pass
    return spec_name, base_file
