#!/usr/bin/python

# Name: checkimage
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
	print './checkimage.py              -- this message'
	print './checkimage.py inputpath       -- read from inputpath, check exif data of the file.'
	
# Fucntion to sequence the files in the folder
def CheckFiles(fn):
	format = exifutl.GetImageFormat(fn)
	createdt = exifutl.GetAttrFromEXIF(fn,'DateTimeOriginal')
	make = exifutl.GetAttrFromEXIF(fn,'Make')
	model = exifutl.GetAttrFromEXIF(fn,'Model')
	gps = exifutl.GetGpsInfoFromEXIF(fn)
	
	print '[%s] TYPE:%s MAKE:%s MODEL:%s DT:%s GPS:%s' % (fn,format,make,model,createdt,gps) 


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
	


