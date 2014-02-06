#!/usr/bin/python

# Name: mergeperloctime
# Version: 1.0
# Author: Steve Wang
# Purpose: predict location of one file
# Output: 

import sys
import os
import pathutl
import datetime
import time
import shutil

# Function to print help for user
def PrintHelp():
	print 'How to use this program'
	print '-----------------------'
	print './mergeperloctime.py              -- this message'
	print './mergeperloctime.py inputpath outputpath       -- read from inputpath, merge per loc and time, write into outputpath'

# Function to get FolderList
def GetFolderList(path):	
	path = pathutl.FormatPath(path)
	list = os.listdir(path)
	folderlist = []
	for x in list:
		if os.path.isdir(path+x):
			if len(x) >10 and x[8] == '_':
				folderlist.append(x)
	return folderlist	

# Function to revert the name of folder
def RevertFolderNameInList(list):
	outlist = []
	for x in list:
		y = x[9:len(x)] +'_'+ x[0:8]
		outlist.append(y)
	return outlist

# Function to soft folder list
def SortFolderList(list):
	outlist = []
	for x in list:
		num = len(outlist)
		if num == 0:
			outlist.append(x)
		else:
			flag = 0
			for index in range(0,num):
				if x < outlist[index]:
					outlist.insert(index,x)
					flag = 1
					break
			if flag == 0:
				outlist.append(x)
	return outlist

# Function to get datetime from filename
def GetDateTimeFromName(name):	
	dt = name[-8:len(name)]
	year = dt[0:4]
	month = dt[4:6]
	day = dt[6:8]
	strdt = '%s:%s:%s' % (year,month,day)
	result = datetime.datetime.fromtimestamp(time.mktime(time.strptime(strdt,'%Y:%m:%d')))
	return result
	
	
# Function to merge folders
def GenerateMergeList(list):
	length = len(list)
	index = 0
	outputlist = []
	while index < length:
		folder = list[index]
		dtfrom = GetDateTimeFromName(folder)
		mergelist = [folder]
		to = index + 1
		while to < length:
			foldernext = list[to]
			dtto = GetDateTimeFromName(foldernext)
			if (folder[0:-9] == foldernext [0:-9]) and ((dtto - dtfrom).days == 1):
				dtfrom = dtto
				mergelist.append(foldernext)
				to = to + 1
			else:
				break
		outputlist.append(mergelist)
		index = to
	return outputlist
	
def main():
	argc = len(sys.argv)
	if argc <= 2:
		PrintHelp()
		exit()
	inputpath = sys.argv[1]
	outputpath = pathutl.FormatPath(sys.argv[2])
	list = GetFolderList(inputpath)
	countbefore = len(list)
	list = RevertFolderNameInList(list)
	list = SortFolderList(list)
	list = GenerateMergeList(list)
	countafter = len(list)
	for x in list:
		start = x[0]
		end = x[len(x)-1]
		foldername = start[-8:len(start)] + '_' + end[-8:len(end)] + '_' + start[0:-9]
#		print foldername,
#		print '[',
#		print len(x),
#		print ']'
#		print '-------------'
		for y in x:
			strfrom = pathutl.FormatPath(inputpath)+y[-8:len(y)]+'_'+y[0:-9]+'/'
			strto = outputpath+foldername
			if not os.path.isdir(strto):
				os.mkdir(strto)
			print strfrom,' => ',strto
			fntocopy = os.listdir(strfrom)
			for f2c in fntocopy:
				if not os.path.isdir(strfrom+f2c):
					shutil.copy2(strfrom+f2c,strto)
	print countbefore, ' folders are merged into ', countafter, 'folders'

if __name__=='__main__':
	main()
	


