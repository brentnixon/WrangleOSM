## code block to process XML data, unbundle colon-structured values, split the element name and attributes into
## dictionaries, validate that the resulting dictionaries are in the correct structure and data type for their
## destination SQL tables, and finally, write the dictionaries to CSV files

import csv
import codecs
from collections import defaultdict, OrderedDict
import pprint
import re
import xml.etree.cElementTree as ET
import cerberus
import schema # note: refers to the schema.py file attached in this directory

OSM_PATH = "Charlotte_AOI.xml"

# CSV files to write to
NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

# define regular expression to compile, for identifying street type, colon-structured values, and problem characters
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# schema to validate dictionaries against
SCHEMA = schema.schema

# right order of columns for each dict/CSV file
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

# list of expected street types, used when identifying problematic street types
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons"]

# dictionary of desired mapping to use when updating street types
mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "Dr": "Drive",
            "Dr.": "Drive",
            "Ext": "Extension",
            "Ext.": "Extension",
            "Ct": "Court",
            "Ct.": "Court",
            "Pl": "Place",
            "Pl.": "Place",
            "Sq": "Square",
            "Sq.": "Square",
            "Ln": "Lane",
            "Ln.": "Lane",
            "Rd": "Road",
            "Rd.": "Road",
            "Trl": "Trail",
            "Trl.": "Trail",
            "Pkwy": "Parkway",
            "Pkwy.": "Parkway",
            "Cmns": "Commons",
            "Cmns.":"Commons"
            }

# function to process each 'tag' sub-element, extracting the attributes, cleaning problematic street types
# and unbundling any colon-structured values
def shape_tag(element, tags, mapping, node_tags_fields=NODE_TAGS_FIELDS, problem_chars=PROBLEMCHARS, lower_colon=LOWER_COLON, default_tag_type='regular'):
    for elem in element.iter(tag="tag"):
        if elem.attrib['k'] == "addr:street":
            m = street_type_re.search(elem.attrib['v'])
            if m:
                street_type = m.group()
                if street_type in expected:
                    continue
                else:
                    old_street_name = elem.attrib['v']
                    street_bits = old_street_name.split(" ")
                    if street_bits[-1] not in mapping:
                        continue
                    else:
                        street_bits[-1] = mapping[street_bits[-1]]
                        elem.attrib['v'] = " ".join(street_bits)
    for elem in element.iter(tag="tag"):
        tag_dict= {}
        for field in node_tags_fields:
            tag_dict[field] = ""
        tag_dict["id"] = element.get("id")
        for a, b in elem.items():
            if a == "k":
                if problem_chars.search(b):
                    continue
                elif lower_colon.search(b):
                    splist = b.split(":", maxsplit=1)
                    tag_dict["key"] = splist[1]
                    tag_dict["type"] = splist[0]
                else:
                    tag_dict["key"] = b
                    tag_dict["type"] = default_tag_type
            elif a == "v":
                    tag_dict["value"] = b
        tags.append(tag_dict)

# function to process and clean elements, extracting node, way, and nd attributes, and processing tags in the same
def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS, way_node_fields=WAY_NODES_FIELDS,\
                  node_tags_fields=NODE_TAGS_FIELDS, problem_chars=PROBLEMCHARS, lower_colon=LOWER_COLON, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""
    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []

    if element.tag == "node":
        for field in node_attr_fields:
            node_attribs[field] = ""
        for a, b in element.items():
            if a in node_attr_fields:
                node_attribs[a] = b
        shape_tag(element, tags, mapping, node_tags_fields=NODE_TAGS_FIELDS, problem_chars=PROBLEMCHARS, lower_colon=LOWER_COLON, default_tag_type='regular') #run the shape tag function on any tag sub-element

    if element.tag == "way":
        for field in way_attr_fields:
            way_attribs[field] = ""
        for a, b in element.items():
            if a in way_attr_fields:
                way_attribs[a]= b
        shape_tag(element, tags, mapping, node_tags_fields=NODE_TAGS_FIELDS, problem_chars=PROBLEMCHARS, lower_colon=LOWER_COLON, default_tag_type='regular') #run the shape tag function on any tag sub-element

        for nd in element.iter(tag="nd"):
            nd_dict= {}
            nd_dict["id"] = element.get("id")
            nd_dict["node_id"] = nd.get("ref")
            nd_dict["position"] = list(element.iter()).index(nd)
            way_nodes.append(nd_dict)
    if element.tag == 'node':
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        return {'way': way_attribs, 'way_tags': tags, 'way_nodes': way_nodes}


# ================================================== #
#               Helper Functions                     #
# ================================================== #

# function to iteratively parse the XML file and yield each element
def get_element(osm_file, tags=('node', 'way', 'relation')):
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

# function to validate if element matches the schema
def validate_element(element, validator, schema=SCHEMA):
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)

        raise Exception(message_string.format(field, error_string))

# extends csv.DictWriter to handle Unicode input
class UnicodeDictWriter(csv.DictWriter, object):
    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #

# function to iteratively process each element in XML file and write to CSVs
def process_map(file_in, validate):

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
            codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
            codecs.open(WAYS_PATH, 'w') as ways_file, \
            codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
            codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()


        count = 0
        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)
                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    process_map(OSM_PATH, validate=True) 
