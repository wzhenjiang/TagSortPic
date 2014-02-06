#!/usr/bin/python

# Name: geoutl
# Version: 1.0
# Author: Steve Wang
# Purpose: Module to aggregate all geographic functions
# Output: 

import sys
import os
import urllib2
from xml.dom.minidom import parseString

#function get Element from xml
def GetXmlElement(dom, tag, index):
	try:
		value = dom.getElementsByTagName(tag)[index].toxml()
		tagStart = '<%s>' % (tag)
		tagEnd = '</%s>' % (tag)
		value = value.replace(tagStart,'').replace(tagEnd,'')
	except Exception,e:
		return tag
	return value


#function get address via reverse geocoder api
def GetAddress(location):
	querystr = 'http://reverse.geocoder.cit.api.heremaps.cn/6.2/reversegeocode.xml?app_id=DemoAppId01082013GAL&app_code=AJKnXv84fjrb0KIHawS0Tg&gen=3&mode=retrieveAddresses&language=zh'
	para = '&prox=%s,100' % (location)
	requesturl = querystr+para
	response = urllib2.urlopen(requesturl)
	data = response.read()
	response.close()
	dom = parseString(data)
	location = dom.getElementsByTagName('Address')[0]

	label = GetXmlElement(location,'Label',0)

	return label
	
#function get address via reverse geocoder api
def GetArea(location):
	querystr = 'http://reverse.geocoder.cit.api.heremaps.cn/6.2/reversegeocode.xml?app_id=DemoAppId01082013GAL&app_code=AJKnXv84fjrb0KIHawS0Tg&gen=3&mode=retrieveAreas&language=zh'
	para = '&prox=%s' % (location)
	requesturl = querystr+para
	response = urllib2.urlopen(requesturl)
	data = response.read()
	response.close()
	dom = parseString(data)
	location = dom.getElementsByTagName('Address')[0]
	
	label = GetXmlElement(location,'Label',0)
	
	try:
		country = GetXmlElement(location,'AdditionalData',0)
		country = country.split('key="CountryName">')[1]
	except Exception, e:
		country = GetXmlElement(location,'Country',0)
	
	state = GetXmlElement(location,'State',0)
	city = GetXmlElement(location,'City',0)
	district = GetXmlElement(location,'District',0)
	label = GetXmlElement(location,'Label',0)

	homecountry = u'\u4e2d\u56fd'
	homecity = u'\u5317\u4eac\u5e02'

	if country != homecountry:
		return '%s_%s' % (country,city)

	if city != homecity:
		return '%s_%s' % (state,city)
		
	if district == 'District':
			return city
	
	return '%s_%s' % (city,district)
		
	
	
	
def main():
	argc = len(sys.argv)
	print GetArea('39.999579,116.467761')
	print GetAddress('39.999579,116.467761')

if __name__=='__main__':
	main()
	


