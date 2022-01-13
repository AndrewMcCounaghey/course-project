#coding=utf-8
# -*- coding: utf_8 -*-

import sys
from collections import OrderedDict
from sys import getdefaultencoding
import codecs
import time
import requests
import re


import csv
import os
c=0
coef=0
count=0
coff=0
arr=[]


with codecs.open(u"Data.txt",'r') as r_file:
	file_reader=r_file.readlines()
	print "Category="
	cat=input()	
	cat=str(cat)
	for row in file_reader:
		a=row.split(';')
		
		if a[2]==cat and a[0]=='1' and a[1]=='0' and a[3]!='0' and a[4]!='0' and a[3]!='' and a[4]!='':

			start_pr=a[3].replace(" ","").replace(",",".")
			end_pr=a[4].replace(" ","").replace(",",".")	
			x=float(start_pr)
			# print x
			y=float(end_pr)
			# print y
			# if 0.00<=x<=49999.99:
			# 	p=x*5
			# 	if p>=y:
			# 		c=1
			# 		arr.append(row)
			# 		coef=((y-x)/x)+coef
			# 		print "coef=",coef
			# 		print row
			# 	else:
			# 		continue

			# if 50000.00<=x<=199999.99:
			# 	c=2
			# 	p=x*5
			# 	if p>=y:
			# 		c=1
			# 		arr.append(row)
			# 		coef=((y-x)/x)+coef
			# 		print "coef=",coef
			# 		print row
			# 	else:
			# 		continue
			# if 200000.00<=x<=499999.99:
			# 	c=3
			# 	p=x*5
			# 	if p>=y:
			# 		c=1
			# 		arr.append(row)
			# 		coef=((y-x)/x)+coef
			# 		print "coef=",coef
			# 		print row
			# 	else:
			# 		continue
			# if 500000.00<=x<=999999.99:
			# 	c=4
			# 	p=x*5
			# 	if p>=y:
			# 		c=1
			# 		arr.append(row)
			# 		coef=((y-x)/x)+coef
			# 		print "coef=",coef
			# 		print row
			# 	else:
			# 		continue
			# if 1000000.00<=x<=1999999.99:
			# 	c=5
			# 	p=x*5
			# 	if p>=y:
			# 		c=1
			# 		arr.append(row)
			# 		coef=((y-x)/x)+coef
			# 		print "coef=",coef
			# 		print row
			# 	else:
			# 		continue
			# if 2000000.00<=x<=4999999.99:
			# 	c=6
			# 	p=x*5
			# 	if p>=y:
			# 		c=1
			# 		arr.append(row)
			# 		coef=((y-x)/x)+coef
			# 		print "coef=",coef
			# 		print row
			# 	else:
			# 		continue
			# if 5000000.00<=x<=9999999.99:
			# 	c=7
			# 	p=x*5
			# 	if p>=y:
			# 		c=1
			# 		arr.append(row)
			# 		coef=((y-x)/x)+coef
			# 		print "coef=",coef
			# 		print row
			# 	else:
			# 		continue
			if 10000000.00<=x:
				c=8	
				p=x*5
				if p>=y:
					c=1
					arr.append(row)
					coef=((y-x)/x)+coef
					#print "coef=",coef
					print row
				else:
					continue
	count=len(arr)				

	print u"Количество=",count
	proc=(coef/count)
	print round((proc*100),1),'%'
	coff=1+proc
	print cat,'|||',c,'|||',round(coff,2)
  	
   
    
