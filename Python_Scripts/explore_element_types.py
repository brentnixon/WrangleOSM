## code block to explore tag type and counts
import xml.etree.cElementTree as ET
import pprint

# function to list what tag names are in the XML file and give their counts
def count_tags(filename):
    things = {}
    for _, val in ET.iterparse(filename):
        if val.tag in things:
            things[val.tag] +=1
        else:
            things[val.tag] = 1
    return things

# execute function on XML file
pprint.pprint(count_tags("Charlotte_AOI.xml"))
