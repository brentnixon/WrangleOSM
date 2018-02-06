## code for getting XML data from OSM using the Overpass API
import requests
def get_XML_data(URL, FILENAME):

    # make the request but have it stream instead of reading all data into memory at once
    r = requests.get(URL, stream=True)

    try:
        # print the URL to debug in event that error gets thrown
        print("Request URL:",r.url)

        # Throw an error for bad status codes
        r.raise_for_status()

        # use iter_lines to parse each line one by one
        events = r.iter_lines()

        # write each line, line by line, into a writable file
        with open (FILENAME, 'w') as f:
            for line in events:
                f.write(line.decode('utf-8'))
                f.write("\n") # this is necessary to maintain the formatting in the file

        # success messages
        print("File write was success!")

    except Exception as e:
        print (e)

    finally:
        r.close()

## code for sample acquisition
SAMPLE_URL = "http://overpass-api.de/api/map?bbox=-80.8676,35.1993,-80.8099,35.2218"
SAMPLE_FILENAME = "Charlotte_sample.xml"
get_XML_data(SAMPLE_URL, SAMPLE_FILENAME)

# code for 50mb size dataset
URL = "http://overpass-api.de/api/map?bbox=-80.8934,35.1157,-80.7368,35.2310"
FILENAME = "Charlotte_AOI.xml"
# get_XML_data(URL, FILENAME)
