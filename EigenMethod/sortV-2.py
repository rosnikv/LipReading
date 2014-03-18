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
        f=open("/home/freestyler/score.txt").read().split('\n')
        f.pop()
        dict={}
        for line in f:
            stringvalue=' '.join(line.split()[1:])
	    #Sprint line.split()[0]
            dict[(line.split()[2])]=stringvalue.split()
	    #stringvalues=sorted(dict.items())[1:3]
	#print dict  		     	
	#for key,value in dict.items():
	#	stringvalues=value.keys()[0]
	#print stringvalues
	
	strings=sorted(dict.keys(),key=lambda k: dict[k][2],reverse=True)

 	#stringvalue= str(sorted(dict.items(), key=lambda x: x[1]) ) 
	#print strings
	#searchObj = re.search( r'(.*) are (.*?) .*', line, re.M|re.I) 
	# Remove anything other than digits
	#string = re.sub(r'\S', "", stringvalue) 
	
	#def extract(stringvalue, sub1, sub2):
	string=strings[0]
	reqstring = string.split("/")[-1].split(".")[0]	
	
	print reqstring      
	file3=open('/home/freestyler/final.txt','w') 
	file3.write('%s' %reqstring)
	#os.system("""./rr.sh""")
		
	
    except ValueError:
            # count was not a number, so silently discard this item
            pass

if __name__ == "__main__":
    main()


