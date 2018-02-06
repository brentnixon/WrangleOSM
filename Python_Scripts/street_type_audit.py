## code block to collect all the values with street information, and to isolate
## all values with problematic street information
import xml.etree.cElementTree as ET
from collections import defaultdict, OrderedDict
import re
import pprint

# define regular expression to identify street types
osmfile = "Charlotte_AOI.xml"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

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

# function to identify a 'k' attribute with street information
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

################
## block to collect any values with street information

# function to identify a record with any street information and add it to a dictionary
def get_any_street_type(all_streets, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        all_streets[street_type].add(street_name)

# function to iterate through XML file, collecting a set of all unique values with street information
def get_all_streets(osm_file):
    osm_file = open(osmfile, "r")
    all_streets = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way" or elem.tag == "relation":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    get_any_street_type(all_streets, tag.attrib['v'])
    osm_file.close()
    return all_streets

##########################
## block to isolate problematic street information

# function to identify a record with unexpected street information and add it to a dictionary
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

# function to iterate through XML file, collecting a set of unique values with unexpected street information
def audit(osm_file):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way" or elem.tag == "relation":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

# function to take a problematic street type and update it to the correct type using the mapping dictionary
def update_name(name, mapping):
    street_bits = name.split(" ")
    if street_bits[-1] in mapping:
        street_bits[-1] = mapping[street_bits[-1]]
    return " ".join(street_bits)

############
# code block executing the above functions

# execute and print results of get_all_streets on the XML file, shows all values with street information
pprint.pprint(dict(get_all_streets(osmfile)))

# execute and print results of audit on the XML file, collects and prints problematic street information
problematic_street_types = audit(osmfile)
pprint.pprint(dict(audit(osmfile)))

# execute the update_name function and print the mapping of old street name to new, updated street name
for st_type, ways in problematic_street_types.items():
    for name in ways:
        better_name = update_name(name, mapping)
        print (name, "=>", better_name)
