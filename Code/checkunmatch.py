#!/usr/bin/python

# Name: checkunmatch
# Version: 1.0
# Author: Steve Wang
# Purpose: check file that is not matched
# Output: 

import sys
import os
import pathutl
import exifutl

# Function to print help for user
def PrintHelp():
	print 'How to use this program'
	print '-----------------------'
	print './checkunmatch.py              -- this message'
	print './checkunmatch.py inputpath       -- read from inputpath, check exif data of the file.'
	
# Fucntion to sequence the files in the folder
def CheckFiles(fn):
	fndt = exifutl.GetAttrFromEXIF(fn,'DateTimeOriginal')
	print fn,' : ',fndt

def main():
	argc = len(sys.argv)
	if argc <= 1:
		PrintHelp()
		exit()
	path = sys.argv[1]
	path = pathutl.FormatPath(path)
	list = os.listdir(path)
	for x in list:
		CheckFiles(path+x)

if __name__=='__main__':
	main()
	


