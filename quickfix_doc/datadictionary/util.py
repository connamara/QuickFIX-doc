import os
ROOT_DOCUMENT_TAG = 'fix'
COMPONENT_TAG = 'component'
COMPONENT_GROUP_TAG = 'group'


def parse_component(comp):
    """Parse Data Dictionary Individual XML Component

    Arguments:
        comp -- XML document element for component
    """
    comp_elems_dict = dict()
    for comp_elem in comp:
        comp_elem_tag = str(comp_elem.tag).strip()
        if comp_elem_tag == 'group':
            group_name = str(comp_elem.attrib['name']).strip()
            group_reqd = parse_bool_yn(str(comp_elem.attrib['required']).strip())
            group_elems_dict = parse_component(comp_elem)
            comp_elems_dict[group_name] = [group_elems_dict, group_reqd]
        else:
            child_elem_name, child_elem_dict = parse_child_elem(comp_elem)
            comp_elems_dict[child_elem_name] = child_elem_dict
    return comp_elems_dict


def parse_components(comps):
    """Parse Data Dictionary XML Component

    Arguments:
        flds -- XML document element for fields
    """
    comps_dict = dict()
    for comp in comps:
        comp_tag = str(comp.tag).strip()
        if comp_tag.lower() != COMPONENT_TAG.lower():
            raise ValueError(comp_tag + " element tag is not equal to " + COMPONENT_TAG)
        comp_elems_dict = parse_component(comp)
        comps_dict[str(comp.attrib['name']).strip()] = comp_elems_dict
    return comps_dict


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
        group_elems_dict = parse_component(child_elem)
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
