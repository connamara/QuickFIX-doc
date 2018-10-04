from . import util
MESSAGE_TAG = 'message'

def parse_messages(msgs, header, trailer):
    """Parse Data Dictionary XML Messages

    Arguments:
        msgs -- XML document element for messages
        header -- Special XML document tag for header message
        trailer -- Special XML document tag for trailer message
    """
    msgs_dict = dict()
    if header is not None:
        msg_elems_dict = dict()
        for msg_elem in header:
            child_elem_name, child_elem_dict = util.parse_child_elem(msg_elem)
            msg_elems_dict[child_elem_name] = child_elem_dict
        msg_top_dict = dict()
        msg_top_dict['elements'] = msg_elems_dict
        msg_top_dict['category'] = "Header/Trailer"
        msg_top_dict['msgtype'] = "HEADER"
        msgs_dict["Standard Message Header"] = msg_top_dict
    if trailer is not None:
        msg_elems_dict = dict()
        for msg_elem in trailer:
            child_elem_name, child_elem_dict = util.parse_child_elem(msg_elem)
            msg_elems_dict[child_elem_name] = child_elem_dict
        msg_top_dict = dict()
        msg_top_dict['elements'] = msg_elems_dict
        msg_top_dict['category'] = "Header/Trailer"
        msg_top_dict['msgtype'] = "TRAILER"
        msgs_dict["Standard Message Trailer"] = msg_top_dict
    for msg in msgs:
        msg_tag = str(msg.tag).strip()
        if msg_tag.lower() != MESSAGE_TAG.lower():
            raise ValueError(msg_tag + " element tag is not equal to " + MESSAGE_TAG)
        msg_elems_dict = dict()
        for msg_elem in msg:
            child_elem_name, child_elem_dict = util.parse_child_elem(msg_elem)
            msg_elems_dict[child_elem_name] = child_elem_dict
        msg_top_dict = dict()
        msg_top_dict['elements'] = msg_elems_dict
        msg_top_dict['category'] = str(msg.attrib['msgcat']).strip()
        msg_top_dict['msgtype'] = str(msg.attrib['msgtype']).strip()
        msgs_dict[str(msg.attrib['name']).strip()] = msg_top_dict
    return msgs_dict
