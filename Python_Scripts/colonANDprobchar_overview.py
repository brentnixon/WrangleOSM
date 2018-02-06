## code block to identify different types of node and way tag key-attribute values, as well as
## identifying colon-structured values and problem characters

import xml.etree.cElementTree as ET
import pprint
import re

# define regular expressions for compiling
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# function to identify values with colons and problem characters
def get_key_type(element, key_vals):
    if element.tag == "tag":
        if lower.search(element.get('k')):
            key_vals["lower"].append(element.get('k'))
        elif lower_colon.search(element.get('k')):
            key_vals["lower_colon"].append(element.get('k'))
        elif problemchars.search(element.get('k')):
            key_vals["problemchars"].append(element.get('k'))
        else:
            key_vals["other"].append(element.get('k'))
    pass
    return key_vals

# function to iterate through each line of XML file and yield dictionary of lists with values of each type
def process_map(filename):
    key_vals = {"lower": [], "lower_colon": [], "problemchars": [], "other": []}
    for _, element in ET.iterparse(filename):
        key_vals = get_key_type(element, key_vals)
    return key_vals

# execute process_map function on XML file
key_vals = process_map('Charlotte_AOI.xml')

# print out different types of values
print("sample of 'lower' values:")
pprint.pprint(key_vals["lower"][0::2100])
print("\n", "sample of 'lower_colon' values:")
pprint.pprint(key_vals["lower_colon"][0::1000])
print("\n", "sample of 'other' values:")
pprint.pprint(key_vals["other"][0::120])
