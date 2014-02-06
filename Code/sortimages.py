#!/usr/bin/python

# Name: sortimages
# Version: 1.0
# Author: Steve Wang
# Purpose: sequence the images, rename them in order
# Output: 

import sys
import os
import pathutl
import exifutl

# Function to print help for user
def PrintHelp():
	print 'How to use this program'
	print '-----------------------'
	print './sortimages.py              -- this message'
	print './sortimages.py inputpath       -- read from inputpath, find all subfolders, find all files in subfolders, sort them and rename in secquence.'
	
# Fucntion to sequence the files in the folder
def SeqFiles(path):
	path = pathutl.FormatPath(path)
	fnlist = os.listdir(path)
	fnlistwithattr = []
	for fn in fnlist:
		if not os.path.isdir(path+fn):
			filedt = exifutl.GetAttrFromEXIF(path+fn,'DateTimeOriginal')	
			fnlistwithattr.append((fn,filedt))
	
	fnlistwithattrinorder = []
	fnlistwithattrinorder.append(fnlistwithattr[0])
	
	for x in range(1,len(fnlistwithattr)):
		for y in range(0,len(fnlistwithattrinorder)):
			if fnlistwithattr[x][1] < fnlistwithattrinorder[y][1]:
				fnlistwithattrinorder.insert(y,fnlistwithattr[x])
				break
		if fnlistwithattr[x][1] >= fnlistwithattrinorder[len(fnlistwithattrinorder)-1][1] :
			fnlistwithattrinorder.append(fnlistwithattr[x])
				
	for x in range(0,len(fnlistwithattrinorder)):
		newname = 'IMAGE%010d.JPG' % (x)
		os.rename(path+fnlistwithattrinorder[x][0],path+newname)
		print fnlistwithattrinorder[x][0],' => ',newname
 

def main():
	argc = len(sys.argv)
	if argc <= 1:
		PrintHelp()
		exit()
	path = sys.argv[1]
	path = pathutl.FormatPath(path)
	list = os.listdir(path)
	for x in list:
		SeqFiles(path+x)

if __name__=='__main__':
	main()
	


