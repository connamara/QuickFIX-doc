from rstcloth import table
from rstcloth import rstcloth


def _produce_element_rows(element_name, element_data, fields, added_components):
    """Generate element rows for fields, components, and nested groups"""
    element_rows = list()
    components_to_add = [comp for comp in added_components]
    is_group = not isinstance(element_data, dict)
    reqd = element_data['required'] if not is_group else element_data[1]
    required = "*" if reqd else ""
    if is_group:
        element_rows.append(["", "*"+element_name+"*", required, "", ""])
        sorted_group_elem_names = sorted([name for name in element_data[0]])
        for group_elem_name in sorted_group_elem_names:
            group_elem_data = element_data[0][group_elem_name]
            element_rows_group, comps_to_add = _produce_element_rows(group_elem_name, group_elem_data, fields, components_to_add)
            for element_row_group in element_rows_group:
                element_row_group[0] = "> "+element_row_group[0]
                element_rows.append(element_row_group)
            for new_comp in comps_to_add:
                if not new_comp in components_to_add:
                    components_to_add.append(new_comp)
    else:
        if element_data['type'] == 'field' and element_name in fields:
            field = fields[element_name]
            tag = rstcloth.RstCloth.inline_link(str(field['number']), "http://fixwiki.org/fixwiki/"+element_name)
            description = str(field['type'])
            if 'values' in field:
                values = field['values']
                sorted_values = sorted([value for value in values])
                for val in sorted_values:
                    val_representation = str(val).strip() + " = " + str(values[val])
                    element_rows.append([tag, element_name, required, description, val_representation])
                    tag = ""
                    element_name = ""
                    required = ""
                    description = ""
            else:
                element_rows.append([tag, element_name, required, description, ""])
        elif element_data['type'] == 'component':
            if not element_name in components_to_add:
                components_to_add.append(element_name)
            link_to_instrument = "`"+element_name+"`_"
            element_rows.append(["", link_to_instrument, required, "*Component*", ""])
    return element_rows, components_to_add


def produce_message_page(message_name, message_content, fields, components):
    """Produce an individual restructuredtext document for an individual message page"""
    d = rstcloth.RstCloth()
    d.title(message_name + " ("+str(message_content['msgtype'])+")")
    # Message Summary
    d.newline()
    t = table.TableData(num_columns=2)
    t.add_header(["MsgType", "Category"])
    t.add_row([message_content['msgtype'], message_content['category'].upper()])
    for table_line in table.RstTable(t).render_table():
        d.content(table_line, wrap=False)
    d.newline()

    #Message Fields
    standard_header = ["Tag", "Field Name", "Req'd", "Data Type", "Acceptable Enums"]
    components_to_add = list()
    d.h2("Fields")
    d.newline()
    t = table.TableData(num_columns=5)
    t.add_header(standard_header)
    table_empty = True
    sorted_element_names = sorted([elem_name for elem_name in message_content['elements']])
    for element_name in sorted_element_names:
        element_rows, new_comps_to_add = _produce_element_rows(element_name, message_content['elements'][element_name], fields, components_to_add)
        for new_comp in new_comps_to_add:
            if not new_comp in components_to_add:
                components_to_add.append(new_comp)
        for element_row in element_rows:
            table_empty = False
            t.add_row(element_row)
    if table_empty:
        t.add_row(["*empty*" for _ in standard_header])
    for table_line in table.ListTable(t).output:
        d.content(table_line, wrap=False)
    d.newline()

    #If there were any components, add those now
    if len(components_to_add) > 0:
        d.h2("Components")
        d.newline()
        processing_components = [comp for comp in components_to_add]
        processed_component_rows = dict()
        while len(processing_components) > 0:
            component = processing_components.pop()
            if not component in processed_component_rows:
                processed_component_rows[component] = dict()
            for comp_elem in components[component]:
                component_data = components[component][comp_elem]
                element_rows, new_comps_to_add = _produce_element_rows(comp_elem, component_data, fields, components_to_add)
                processed_component_rows[component][comp_elem] = element_rows
                for new_comp in new_comps_to_add:
                    if not new_comp in components_to_add:
                        components_to_add.append(new_comp)
                        processing_components.append(new_comp)
        sorted_component_names = sorted([name for name in processed_component_rows])
        for component in sorted_component_names:
            d.h4(component)
            d.newline()
            t2 = table.TableData(num_columns=5)
            t2.add_header(standard_header)
            sorted_component_elems = sorted([elem for elem in processed_component_rows[component]])
            for comp_elem in sorted_component_elems:
                element_rows = processed_component_rows[component][comp_elem]
                for element_row in element_rows:
                    t2.add_row(element_row)
            for table_line in table.ListTable(t2).output:
                d.content(table_line, wrap=False)
            d.newline()

    return '\n'.join(d.data)
