#!/usr/bin/env python
import re
from operator import itemgetter
import sys
from itertools import groupby
from operator import itemgetter
import sys
import os
def main(seperator='\t'):

    try: 
        f=open("/home/hduser/score.txt").read().split('\n')
        f.pop()
        dict={}
        for line in f:
            stringvalue=' '.join(line.split()[1:])
            dict[float(line.split()[0])]=stringvalue
 	stringvalue= str(max(dict.items(), key=lambda x: x[0]) )   
	#searchObj = re.search( r'(.*) are (.*?) .*', line, re.M|re.I) 
	# Remove anything other than digits
	#string = re.sub(r'\D', "", stringvalue) 
	
	#def extract(stringvalue, sub1, sub2):

	string = stringvalue.split("eigenmean/")[-1].split(".")[0]	
	
	print string      
	file3=open('/home/hduser/final.txt','w') 
	file3.write('%s' %string)
	#os.system("""./rr.sh""")
		
	
    except ValueError:
            # count was not a number, so silently discard this item
            pass

if __name__ == "__main__":
    main()


