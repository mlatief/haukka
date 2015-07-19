import xml.etree.ElementTree as ET


def convert_xml_to_dict(dict_mapping, xml_text):
    """
    Build a dict object by populating dictionary fields with the xml extracted using
    provided XPath which should be relative to root element!

    Examples:
    ```
    xml: <ct><title>sample trial title</title><purpose>sample trial purpose</purpose></ct>
    mapping: {'title': './title', 'purpose':'./purpose'}
    ```

    return :
    ```
    {'title': 'sample trial title', 'purpose':'sample trial purpose'}
    ```

    Note: XPath is specified relative to root XML element.

    Supports lists and nested dictionaries.

    :param dict_mapping:
        Mapping of dict objects and corresponding XPaths
    :param xml_text:
        XML text to process
    :return:
        Dictionary object populated with the data
    """
    d = {}
    root = ET.fromstring(xml_text)
    for (k,v) in dict_mapping.iteritems():
        if isinstance(v, str):
            e = root.find(v)
            if e is not None:
                d[k] = e.text
            else:
                d[k] = None

        elif isinstance(v, list):
            e = root.findall(v[0])
            d[k] = []
            for i in e:
                d[k].append(i.text)

        elif isinstance(v, dict):
            subd = convert_xml_to_dict(v, xml_text)
            d[k] = subd

    return d
