import os
from rstcloth import rstcloth
from . import produce_pages


def make_restructured_text(spec_name, base_file, data_dict_xml_path, output_path, msgs, comps, fields):
    """Make restructuredtext documents for Sphinx consumption"""
    data_per_file = dict()
    # Construct base document header
    d = rstcloth.RstCloth()
    d.title(spec_name + " | " + base_file)
    d.newline()

    # Copy data dictionary as-is into the output path
    with open(data_dict_xml_path, mode='r') as data_dict_file:
        data_per_file[os.path.join(output_path, base_file)] = data_dict_file.read()
    d.h2("Data Dictionary Source")
    d.content(rstcloth.RstCloth.role("download", base_file))
    d.newline()

    # Categorize all the messages
    msg_with_categories = dict()
    for msg_name in msgs:
        # Categorize the message
        msgtype = msgs[msg_name]['category']
        if not msgtype in msg_with_categories:
            msg_with_categories[msgtype] = list()
        msg_with_categories[msgtype].append(msg_name)
        # Generate the data
        msg_file_data = produce_pages.produce_message_page(msg_name, msgs[msg_name], fields, comps)
        data_per_file[os.path.join(output_path, "Messages", msg_name + ".rst")] = msg_file_data

    # Generate table of contents
    for msg_category in msg_with_categories:
        d.h2("Messages - "+msg_category.upper())
        msgs_content = ["Messages/" + str(key) for key in msg_with_categories[msg_category]]
        d.directive(name="toctree", content=msgs_content)
        d.newline()
    data_per_file[os.path.join(output_path, "index.rst")] = '\n'.join(d.data)

    # Generate conf.py for sphinx
    conf_py = list()
    conf_py.append("project = '" + base_file + "'")
    conf_py.append("author = '" + spec_name + "'")
    conf_py.append("source_suffix = '.rst'")
    conf_py.append("master_doc = 'index'")
    conf_py.append("language = None")
    conf_py.append("html_theme = 'bizstyle'")
    conf_py.append("exclude_patterns = ['Thumbs.db', '.DS_Store']")
    conf_py.append("pygments_style = None")
    data_per_file[os.path.join(output_path, "conf.py")] = '\n'.join(conf_py)
    return data_per_file
