#!/usr/bin/python

# Name: exifutl
# Version: 1.0
# Author: Steve Wang
# Purpose: Get Geo Info from EXIF
# Output: EXIF

import sys
import os
from PIL import Image
from PIL.ExifTags import TAGS

#function to read EXIF 
def get_exif(fn):
    ret = {}
    imageobject = Image.open(fn)
    info = imageobject._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

#function to get image format
def GetImageFormat(fn):
    ret = {}
    imageobject = Image.open(fn)
    return imageobject.format
	
# Function to get GPSInfo From EXIF of the file
def GetGpsInfoFromEXIF(filename):
	gpsdata = GetAttrFromEXIF(filename,'GPSInfo')
	if not gpsdata:
		return None
	try:
		latdegree = float(gpsdata[2][0][0])/float(gpsdata[2][0][1])
		latminute = float(gpsdata[2][1][0])/float(gpsdata[2][1][1])
		latsecond = float(gpsdata[2][2][0])/float(gpsdata[2][2][1])
		
		londegree = float(gpsdata[4][0][0])/float(gpsdata[4][0][1])
		lonminute = float(gpsdata[4][1][0])/float(gpsdata[4][1][1])
		lonsecond = float(gpsdata[4][2][0])/float(gpsdata[4][2][1])
		
		latitude = latdegree + (latminute + latsecond/60 )/60
		if gpsdata[1] == 'S':
			latitude = 0 - latitude
		longitude = londegree + (lonminute + lonsecond/60 )/60
		if gpsdata[3] == 'W':
			longitude = 0 - longitude
		
		location = '%f,%f' % (latitude,longitude)		
		return location
	except Exception, e:
#		print filename,
#		print ' failed to calculate location'
		return None

# Function to get GPSInfo From EXIF of the file
def GetAttrFromEXIF(filename,attr):
	try:
		exifdata = get_exif(filename)
		try:
			result = exifdata[attr]
			return result
		except Exception, e:
#			print filename,
#			print 'does not have ',
#			print attr
			return None
	except Exception, e:
#		print filename,
#		print 'is not a picture with exif'
		return None

		
def main():
	print "there isn't unit test"

if __name__=='__main__':
	main()
	


