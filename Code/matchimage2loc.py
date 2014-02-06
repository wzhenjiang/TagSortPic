#!/usr/bin/python

# Name: matchimage2loc
# Version: 1.0
# Author: Steve Wang
# Purpose: predict location of one file
# Output: 

import sys
import os
import pathutl
import exifutl
import datetime
import time
import shutil

# Function to print help for user
def PrintHelp():
	print 'How to use this program'
	print '-----------------------'
	print './matchimage2loc.py              -- this message'
	print './matchimage2loc.py inputpath indexpath       -- read from inputpath and match to indexpath folders, if match, copy over'

# Function to get DTList
def GetDTList(path):	
	path = pathutl.FormatPath(path)
	list = os.listdir(path)
	dtlist = []
	for x in list:
		dtlist.append(time.strptime(exifutl.GetAttrFromEXIF(path+x,'DateTimeOriginal'),'%Y:%m:%d %H:%M:%S'))
	return dtlist	
	
# Function to generate candidate list
def GenerateCandidateList(path,dt):
	path = pathutl.FormatPath(path)
	list = os.listdir(path)
	loclist = []
	for folder in list:
		if folder[0:8] == dt:
			dtlist = GetDTList(path+folder)
			loclist.append([folder,dtlist])
	return loclist

# Function to match file named as fn to indexpath
def predict(fn,indexpath):
	dt = exifutl.GetAttrFromEXIF(fn,'DateTimeOriginal')
	candidatelist = GenerateCandidateList(indexpath,dt.replace(':','')[0:8])
	dtDateTime = datetime.datetime.fromtimestamp(time.mktime(time.strptime(dt,'%Y:%m:%d %H:%M:%S')))
	folderto = None
	dis = 3600*24
	for folderdt in candidatelist:
		for fndt in folderdt[1]:
			fndtcal = datetime.datetime.fromtimestamp(time.mktime(fndt))
			if dis > abs((dtDateTime-fndtcal).seconds) :
				dis = abs((dtDateTime-fndtcal).seconds)
				folderto = folderdt[0]
	return [folderto,dis]

#Function to read from path, find all files in subpath, match them to index path	
def Analyze(path,indexpath):
	path = pathutl.FormatPath(path)
	indexpath = pathutl.FormatPath(indexpath)
	list = os.listdir(path)
	countmatch  = 0
	countunmatch = 0
	for dr in list:
		folder = path+dr
		if os.path.isdir(folder):
			folder = pathutl.FormatPath(folder)
			files = os.listdir(folder)
			for fn in files:
				fn = folder+fn
				if not os.path.isdir(fn):
					result = predict(fn,indexpath)
					print fn,
					print result[1],
					print 'Match[',
					if result[1] < 3600:
						print 'Perfect',
					elif result[1] < 3600*4:
						print 'Good',
					else:
						print 'Poor',
					print ']',
					print ' => ',
					print result[0]
					if result[1] < 3600*24:
						shutil.copy2(fn, indexpath+result[0])
						countmatch = countmatch + 1
					else:
						if not os.path.isdir(indexpath+'unmatch'):
							os.mkdir(indexpath+'unmatch')
						shutil.copy2(fn, indexpath+'unmatch')
						countunmatch = countunmatch + 1
	print countmatch,' files from ', len(list),' folders are matched'
	print countunmatch, ' files are not matched'
	
def main():
	argc = len(sys.argv)
	if argc <= 2:
		PrintHelp()
		exit()
	path = sys.argv[1]
	indexpath = sys.argv[2]
	Analyze(path,indexpath)

if __name__=='__main__':
	main()
	


