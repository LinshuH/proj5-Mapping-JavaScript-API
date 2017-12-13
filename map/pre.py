"""
Pre-process a syllabus (class schedule) file. 

"""

import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)



def process(raw):
    """
    Line by line processing of syllabus file.
    The poi file contains pois that contain description,lat,long
    raw: the name of the text file that been read
    entry is a temporary dictionary to represent each poi
    cooked is a list that contain all the pois in a text string format.
    """
    entry = {}
    cooked = []
    
    for line in raw:
    	line = line.strip()
    	if len(line) !=0 and line[0] !="#" :
    		logging.info("Line: {}".format(line))
    		parts = line.split(",")
    		logging.info("Part: {}".format(parts))
    		description = parts[0]
    		lat = parts[1]
    		lng = parts[2]
    		
    		entry["des"] = description
    		entry["latlng"] = { "lat":lat, "lng":lng }
    		#entry["lng"] = lng
    		logging.info("Entry: {}".format(entry))
    		cooked.append(entry)
    		entry = {}
    logging.info("cooked: {}".format(cooked))
    return cooked

def main():
    f = open("poi.txt")
    parsed = process(f)
    print(parsed)
 

if __name__ == "__main__":
    main()
 
