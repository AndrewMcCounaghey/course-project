#coding=utf-8
# -*- coding: utf_8 -*-

from selenium import webdriver
#from lib2to3.tests.support import driver
driver=webdriver.Firefox(executable_path=r'c:\Python27\geckodriver.exe')
#driver=quit()
import syscmd
import time
import requests
import re
from selenium.webdriver.common.keys import Keys
from add_ff import get_profile_path
import csv
#from FedresData import FedresData


#with open('c:\work\modx_1_prodazha(1).csv') as f:
 #   reader = csv.reader(f)
    #headers = next(reader)
    #print('Headers: ', headers)
  #  for inn in reader:
   #     print(inn)
        
#f=FedresData
#f.GetData(inn)

 
    
   # for inn in reader:
    #	print(inn)
    	#проверка на Е
    	#list_num = []
    	#if inn.	find(u"E")>0:
    	#	continue
    		    
  # 	f.GetData(inn)
      


#import Tor


class FedresData:
	def __init__(self):
		firefoxProfile = get_profile_path("default")
		self.driver = webdriver.Firefox(firefoxProfile)

		firefoxProfile = get_profile_path("default")
		self.driver2 = webdriver.Firefox(firefoxProfile)

#		self.driver = Tor.getTor()
#		self.driver2 = Tor.getTor()

		self.hrefs_file = {}
		#self.names_file = []
		self.adress_dolgnik = ""
		self.region_dolgnik = ""
		self.prev_inn=0
		self.prev_innOrgTorg=0
		self.prevNameOrg = ""
		self.prev_phoneOrgTorg=0


	
	def Stop(self):
		self.driver.quit()
		self.driver2.quit()
		
		

	def GetPhone(self, name_org):
		name_org = name_org.strip('\t').strip('\n')
		print "GetPhone for  = "#,name_org

		if name_org==self.prevNameOrg:
			return self.prev_phoneOrgTorg

		self.prev_phoneOrgTorg = ""
		try:
			self.driver.get("http://bankrot.fedresurs.ru/TradeOrganizers.aspx")

			el = self.driver.find_element_by_id("ctl00_cphBody_tbOrgName")
			el.clear()
			el.send_keys(name_org)
			el.send_keys(Keys.RETURN)
			time.sleep(0.5)
			t = 0
			while t<5:
				#все теперь парсим данные
				try:
					el = self.driver.find_element_by_id("ctl00_cphBody_gvTradeOrganizers")
					el = el.find_element_by_xpath(".//a[@href]")
					self.driver.get(el.get_attribute("href"))
					t+=5
				except:
					time.sleep(0.5)
					t+=1

			self.prev_phoneOrgTorg = self.driver.find_element_by_id("ctl00_cphBody_trPhone").get_attribute('textContent').replace(u"Телефон","").strip()

		except:
			fio = name_org.split(" ")
			if len(fio)==3:
				try:
					#print len(fio)
					self.driver.find_element_by_id("ctl00_cphBody_rblTradeOrganizerType_1").click()
					time.sleep(0.2)
					el = self.driver.find_element_by_id("ctl00_cphBody_tbPrsLastName")
					el.clear()
					el.send_keys(fio[0])
					el = self.driver.find_element_by_id("ctl00_cphBody_tbPrsFirstName")
					el.clear()
					el.send_keys(fio[1])
					el = self.driver.find_element_by_id("ctl00_cphBody_tbPrsMiddleName")
					el.clear()
					el.send_keys(fio[2])
					self.driver.find_element_by_id("ctl00_cphBody_btnSearch").click()
					time.sleep(0.5)
					el = self.driver.find_element_by_id("ctl00_cphBody_gvTradeOrganizers")
					el = el.find_element_by_xpath(".//a[@href]")
					self.driver.get(el.get_attribute("href"))
					self.prev_phoneOrgTorg = self.driver.find_element_by_id("ctl00_cphBody_trPhone").get_attribute('textContent').replace(u"Телефон","").strip()

				except:
					self.prev_phoneOrgTorg =""
					print "error phone 2"
			else:
				self.prev_phoneOrgTorg =""


		self.prevNameOrg = name_org

		return self.prev_phoneOrgTorg
		

	def GetData(self, inn):
		
		inn = inn.strip('\t').strip('\n').replace(" ","")
		print "GetDocs for inn = "+str(inn)
		if inn==self.prev_inn:
			return True
		
		self.hrefs_file = {}
		#self.names_file = []
		self.adress_dolgnik = ""
		self.region_dolgnik = ""

		if len(inn)<5:
			print "no inn"
			return True

		f = False
		# while f==False:
		# 	try:
		# 		r = requests.post("http://bankrot.fedresurs.ru/",verify=False, timeout=30)
		# 		print r
		# 		if r.status_code == 200:
		# 			f=True
		# 			break
		# 		time.sleep(30)
		# 	except:
		# 		print(sys.exc_info())
		# 		continue


		i =0
		while i<2:
			try:
			#	self.driver.get("ya.ru")
				self.driver.get("http://bankrot.fedresurs.ru/DebtorsSearch.aspx")
			
				print 'input inn'
				if len(inn)>10:
					self.driver.find_element_by_id("ctl00_cphBody_rblDebtorType_1").click()
					time.sleep(3)

					#el = self.driver.find_element_by_id("ctl00_cphBody_OrganizationCode1_CodeTextBox")
					el = self.driver.find_element_by_id("ctl00_cphBody_PersonCode1_CodeTextBox")
				else:
					self.driver.find_element_by_id("ctl00_cphBody_rblDebtorType_0").click()
					time.sleep(3)

					#el = self.driver.find_element_by_id("ctl00_cphBody_PersonCode1_CodeTextBox")
					el = self.driver.find_element_by_id("ctl00_cphBody_OrganizationCode1_CodeTextBox")



			#	print "send search button"
				el.clear()
				time.sleep(2)
				el.send_keys(inn)
				el.send_keys(Keys.RETURN)
				time.sleep(5)
				#self.driver.find_element_by_id("ctl00_cphBody_btnSearch").click()
				t = 0
				while t<5:
					#все теперь парсим данные
					try:
						#print "ctl00_cphBody_gvDebtors"
						el = self.driver.find_element_by_id("ctl00_cphBody_gvDebtors")
						el = el.find_element_by_xpath(".//a[@href]")
						self.driver.get(el.get_attribute("href"))
						inn2 = self.driver.find_element_by_id("ctl00_cphBody_lblINN").get_attribute('textContent').replace(u"ИНН","").strip()
						snils = self.driver.find_element_by_id("ctl00_cphBody_lblSNILS").get_attribute('textContent').replace(u"СНИЛС","").replace(u"-","").replace(u" ","").strip()

						if inn2!=inn and snils!=inn:
							print inn2, "not good INN = ",inn
							t-=1
							continue
						t+=5
					except:
						time.sleep(1)
						t+=1
			#	print "address"
				self.adress_dolgnik = self.driver.find_element_by_id("ctl00_cphBody_trAddress").get_attribute('textContent').replace(u"Адрес","").replace(u"Место жительства","").strip()
				#print self.adress_dolgnik
				self.region_dolgnik = self.driver.find_element_by_id("ctl00_cphBody_trRegion").get_attribute('textContent').replace(u"Регион","").strip()
				#print self.region_dolgnik

				curPage = 1

				#driver.execute_script()
				fl = True
				while fl==True:
				#	print "start parse page"
					try:
						tableMes= self.driver.find_element_by_id("ctl00_cphBody_gvMessages")
					except:
						time.sleep(2)
						try:
							tableMes= self.driver.find_element_by_id("ctl00_cphBody_gvMessages")
						except:
							time.sleep(2)
				#			print "TRY 3 ctl00_cphBody_gvMessages"
							tableMes= self.driver.find_element_by_id("ctl00_cphBody_gvMessages")
				#	print "search link"
					links = tableMes.find_elements_by_xpath(".//a[@href]")
				#	print "parse links"
					for link in links:
						try:
							#print "get txt"
							txt = link.get_attribute('textContent').lower()
						#11	print "search OCENKA"
							if txt.find(u"оцен")>0 or txt.find(u"нвент")>0 or txt.find(u"ное сообщение")>0 or txt.find(u"определении начальной продажной цены"):
								#print txt
								url = link.get_attribute('href')

								if url.find("javascript")>=0:
									continue
								#print url
								self.hrefs_file[url]=link.get_attribute('textContent').strip().replace('\t',"").replace('\n',"")
								if url.find("MessageWindow")>0:

									#сохраням ссылку на это окно
									if txt.find(u"оцен")>=0:
										self.hrefs_file[url]=u"Отчет об оценке"
									if txt.find(u"нвент")>=0:
										self.hrefs_file[url]=u"Инвентаризационная опись"
									if txt.find(u"ное сообщение")>=0:
										self.hrefs_file[url]=u"Иное сообщение"

									if txt.find(u"определении начальной")>=0:
										self.hrefs_file[url]=u"Иное сообщение"

									self.driver2.get(url)
									lls = self.driver2.find_elements_by_xpath(".//a[@class='Reference']")
									for s in lls:
										if s.get_attribute("href").find("javascript")<0:
											self.hrefs_file[s.get_attribute("href")]=s.get_attribute("textContent").strip().replace('\t',"").replace('\n',"")


								# 	r = requests.post(url, verify=False)
								# 	txt = r.text
								# 	s = u'<a class="Reference" href="'
								# 	idx = txt.find(s)
								# 	while idx>0:
								# 		txt = txt[idx+len(s):]
								# 		idx2 = txt.find('">')
								# 		hf = txt[:idx2]
								# 		txt = txt[idx2+2:]
								# 		nf = txt[:txt.find('</a>')].strip("\t\n")
								# #		print "nf = ",nf
								# 		idx = txt.find(s)									
										
								# 		if hf.find(u"javascript")<0:
								# 			if hf.find(u"Down")==0:
								# 				hf = "http://bankrot.fedresurs.ru/"+hf

								# 			hf = hf.replace("&amp;", "&")
								# 			hf = hf.replace("'", "\"")
								# 		#	print "hf =", hf
								# 			#self.hrefs_file.append(hf)

								# 			self.hrefs_file[hf]=nf
								# 			#self.names_file.append(nf)

						except:
						#	print "error parse links"
							f=""

					#print "parse pager"
					try:
						pager = tableMes.find_element_by_xpath(".//tr[@class='pager']")
					except:
						pager = None

					fl = False
					if pager!=None:
						els = pager.find_elements_by_xpath(".//a[@href]")
						#print len(els)
						curPage+=1
						fs = "Page$"+str(curPage)+"')"
#						print fs

						for el in els:
						#	print el.get_attribute("href")
							if el.get_attribute("href").find(fs)>0:
								try:
									el.click()
									time.sleep(7)
									fl = True
						#			print "after click"
									break
								except:
						#			print "error click nexpage"
									fl = False
					else:
						fl = False

					#print "end iteration"

				#print self.names_file
			except:
				#print(sys.exc_info())
				print "Error FedresData parsing"
			i=i+1

		print self.hrefs_file
		self.prev_inn = inn
		return True








	
	