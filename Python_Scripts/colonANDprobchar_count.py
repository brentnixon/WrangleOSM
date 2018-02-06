## code block to identify and count attribute keys with colon structure or problematic characters

import xml.etree.cElementTree as ET
import pprint
import re

# define regular expressions for compiling
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# function to give a count of each of the four tag categories
def count_key_type(element, keys):
    if element.tag == "tag":
        if lower.search(element.get('k')):
            keys["lower"] += 1
        elif lower_colon.search(element.get('k')):
            keys["lower_colon"] += 1
        elif problemchars.search(element.get('k')):
            keys["problemchars"] += 1
        else:
            keys["other"] += 1
    pass
    return keys

# function to iteratively process lines in XML file and yield dictionary with count of key types
def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = count_key_type(element, keys)
    return keys

# execute process_map on XML file
keys = process_map('Charlotte_AOI.xml')
pprint.pprint(keys)
