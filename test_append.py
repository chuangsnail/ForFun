#!/usr/bin/env python

### Description : 
### 	find the flag and append something after the flag in that file

import argparse
import os
from sys import argv
from array import array

def do_app( args ) :

	parser = argparse.ArgumentParser( "append something after some flag" )
	parser.add_argument( '-f', '--falgstr', dest='flag_str', type=str, required=True )
	parser.add_argument( '-a', '--addstr', dest='add_str', type=str, required=True )

	opt = parser.parse_args( args[1:] )

	f = open("to_do_list.txt", "r")
	contents = f.readlines()
	f.close()

	flag = -1
	for i in range( len(contents) ):
		if contents[i].strip() == opt.flag_str :		#use strip() to strip out '\n' and ' '
			flag = i
			break
	
	contents.insert( int( flag + 1 ), ( opt.add_str + "\n" ) )

	f = open("to_do_list.txt", "w")
	contents = "".join( contents )
	f.write( contents )
	f.close()

if __name__ == '__main__':
	do_app( argv );

