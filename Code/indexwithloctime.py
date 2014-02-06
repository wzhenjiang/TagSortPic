#!/usr/bin/python

# Name: imagemgr
# Version: 1.0
# Author: Steve Wang
# Purpose: manage images files with location intelligence
# Output: organized images

import sys
import os
import pathutl
import geoutl
import exifutl

# Function to print help for user
def PrintHelp():
	print 'How to use this program'
	print '-----------------------'
	print './indexwithloctime.py              -- this message'
	print './indexwithloctime.py inputpath outputpath       -- read from inputpath and index with location and datetime into outputpath'

# Function to format folder with DateTime and Area
def ConstructFolder(dt,area):
	list = dt.split(' ')
	part1 = list[0]
	part1 = part1.replace(':','')
	part2 = area
	if len(part2) < 1:
		return part1
	return '%s_%s' % (part1,part2)
	
# Function to rename those files
def Proceed(inputpath, outputpath, pending):
	inputpath = pathutl.FormatPath(inputpath)
	outputpath = pathutl.FormatPath(outputpath)
	pending = outputpath + pathutl.FormatPath(pending)

	filenames = os.listdir(inputpath)
	num = len(filenames)
	if num <=0:
		return

	x = 0
#	folders = inputpath.ListFolders(inputpath)

	countloc = 0
	countdt = 0
	countpending = 0

	while x < num:
		filename = inputpath + filenames[x]
		fnDateTime = exifutl.GetAttrFromEXIF(filename,'DateTimeOriginal')
		location = exifutl.GetGpsInfoFromEXIF(filename)

		if location:
			address = geoutl.GetAddress(location)
			area = geoutl.GetArea(location)
			print x,
			print '/',
			print num,
			print ' [' + filename + ']:',
			print address,
			print ' => ',
			folder = ConstructFolder(fnDateTime,area)
			print folder
			pathutl.AddFile(filename,folder,outputpath)
			countloc = countloc + 1
		elif fnDateTime:
			print x,
			print '/',
			print num,
			print ' [' + filename + ']:',
			print 'X =>',
			folder = ConstructFolder(fnDateTime,'')
			print pending+folder
			pathutl.AddFile(filename,folder,pending)
			countdt = countdt + 1
		else:
			print x,
			print '/',
			print num,
			print ' [' + filename + ']:',
			print 'X =>',
			print pending
			pathutl.AddFile(filename,'.',pending)
			countpending = countpending + 1
		x = x+1
	print countloc,' are positioned'
	print countdt,' are datetimed'
	print countpending,' are w/o necessary info'
	
def main():
	argc = len(sys.argv)
	if argc <= 2:
		PrintHelp()
		exit()
	inputpath = sys.argv[1]
	outputpath = sys.argv[2]
	print 'read from ' + inputpath
	Proceed(inputpath,outputpath,'pending')

if __name__=='__main__':
	main()
	


