"""
Pre-process a syllabus (class schedule) file. 

"""

import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)



def process(raw):
    """
    Line by line processing of syllabus file.  Each line that needs
    processing is preceded by 'head: ' for some string 'head'.  Lines
    may be continued if they don't contain ':'.  If # is the first
    non-blank character on a line, it is a comment ad skipped. 
    """
    field = None
    entry = { }
    cooked = [ ] 

    for line in raw:
        log.debug("Line: {}".format(line))
        line = line.strip()  # Line is every line in the txt file(raw)
        if len(line) == 0 or line[0]=="#" :
            log.debug("Skipping")
            continue

       # parts = line.split(':')  # parts contain two parts, term before :(field) and after column(content).
       # print(parts)

        elif len(line) != 0: 
            field = parts[0]         #description/latitude/longitude
            content = parts[1]       #name or the number
            entry[field] = content 
            print (entry)
        else:
            raise ValueError("Trouble with line: '{}'\n".format(line) + 
                "Split into |{}|".format("|".join(parts)))

        if entry:
            cooked.append(entry)
            entry = {} 
    return cooked


def main():
    f = open("poi.txt")
    parsed = process(f)
    print(parsed)
 

if __name__ == "__main__":
    main()
 
