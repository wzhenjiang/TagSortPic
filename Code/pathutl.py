#!/usr/bin/python

# Name: pathutl
# Version: 1.0
# Author: Steve Wang
# Purpose: archive file into right folder according to location and Datetime
# Output: 

import os
import sys
import shutil

# Function to standardize path format
def FormatPath(path):
	if len(path) < 1:
		return path
	while path[-1] == ' ':
		path = path[0:-1]
	if len(path) < 1:
		return path
	if path[-1] != '/':
		path = path + '/'
	return path
	
# Function to list folders for assigned path
def ListFolders(path):
	path = FormatPath(path)
	list = []
	filenames = os.listdir(path)
	for fn in filenames:
		if os.path.isdir(path+fn):
			list.append(fn.decode(sys.getfilesystemencoding()))
	return list
	

# Function to add file into folder under outpath
def AddFile(filename, dirname, outpath):
	outpath = FormatPath(outpath)
	if not os.path.isdir(outpath):
		os.mkdir(outpath)
	list = ListFolders(outpath)
	for fn in list:
		if dirname == fn:
			shutil.copy2(filename, outpath+dirname)
			return 0
	try:
		if not os.path.isdir(outpath+dirname):
			os.mkdir(outpath+dirname)
		shutil.copy2(filename, outpath+dirname)
	except Exception,e:
		print filename, ' => ', outpath,dirname, [Failed]
		print e
	return 1