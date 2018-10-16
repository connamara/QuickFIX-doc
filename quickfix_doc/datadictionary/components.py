from . import util
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
            group_reqd = util.parse_bool_yn(str(comp_elem.attrib['required']).strip())
            group_elems_dict = parse_component(comp_elem)
            comp_elems_dict[group_name] = [group_elems_dict, group_reqd]
        else:
            child_elem_name, child_elem_dict = util.parse_child_elem(comp_elem)
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
