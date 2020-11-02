FIELD_TAG = 'field'
FIELD_VALUE_TAG = 'value'


def parse_fields(flds):
    """Parse Data Dictionary XML Fields

    Arguments:
        flds -- XML document element for fields
    """
    fields_dict = dict()
    for elem in flds:
        elem_tag = str(elem.tag).strip()
        if elem_tag.lower() != FIELD_TAG.lower():
            raise ValueError(elem_tag + " element tag is not equal to " + FIELD_TAG)
        elem_dict = dict()
        elem_dict['type'] = str(elem.attrib['type']).upper()
        elem_dict['number'] = int(elem.attrib['number'])
        elem_dict['description'] = elem.attrib['description'] if 'description' in elem.attrib else ''
        elem_values = dict()
        for elem_value in elem:
            elem_value_tag = str(elem_value.tag).strip()
            if elem_value_tag.lower() != FIELD_VALUE_TAG.lower():
                raise ValueError(elem_value_tag + " element value tag is not equal to " + FIELD_VALUE_TAG)
            elem_value_enum = str(elem_value.attrib['enum']).strip()
            elem_value_desc = str(elem_value.attrib['description']).strip()
            elem_values[elem_value_enum] = elem_value_desc
        if elem_values:
            elem_dict['values'] = elem_values
        fields_dict[str(elem.attrib['name']).strip()] = elem_dict
    return fields_dict
