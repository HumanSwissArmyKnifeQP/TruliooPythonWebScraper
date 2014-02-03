import urllib2
from lxml import html
import requests
import csv
#get html of the page
def getHtml():
	page = requests.get('http://www.area-codes.org.uk/')
	tree = html.fromstring(page.text)
	return tree

#get all the links we need to crawl
def getLinkElements(tree):
	urls = tree.xpath('//ul[@class="nod"]//li//a/@href')
	return urls

def getCityName(citytree):
	#get header where city name is
	citynamefull = citytree.xpath('//div[@id="big_l"]//h2/text()')
	#split the text where as "phone" appears after  the city name
	citynamefull = citynamefull[0].split("phone")
	#get cityname
	cityname =  citynamefull[0]
	return cityname

def numberOfDigits(numberofdigitstree):
	numberofdigitspelements = numberofdigitstree.xpath('//div[@id="big_l"]//p/text()')
	#because there are several <p> tags, we need to iterate through to see if they tell us how many digits are used
	for pelements in numberofdigitspelements:
		if pelements.find('seven') != -1:
			return '7'
		elif pelements.find('six') != -1:
			return '6'
		elif pelements.find('eight') != -1:
			return '8'
		elif pelements.find('nine') != -1:
			return '9'
		elif pelements.find('five')  != -1:
			return '5'			
		
	return None
	#citynamefull = citynamefull[0].split("phone")
	#cityname =  citynamefull[0]
	#return cityname	

# this function is used to get area code 
def getAreaCode(areacodetree):
	areacodeelements = areacodetree.xpath('//div[@id="big_l"]//h1/text()')
	areacodestring = areacodeelements[0]
	actualareacode = areacodestring.split('area code')[0]
	return actualareacode

def crawlURL(urlstocrawl):
	valuescrawled=  []
	for url in urlstocrawl:
		#get page from url
		page = requests.get('http://www.area-codes.org.uk/'+url)
		#transform to html
		tree= html.fromstring(page.text)
		#get city name
		cityname  = getCityName(tree)
		#get number of digits
		numdigits = numberOfDigits(tree)
		#get the areacode
		areacode = getAreaCode(tree)
		
		#check to see if we have a complete element. If it doesnt return complete element then dont add to valuescrawled
		if areacode != None:
			#remove all trailing whitespaces

			try:
				cityname = cityname.strip()
				numdigits= numdigits.strip()
				areacode = areacode.strip()
			except:
				pass	
			#create a new list element with all values
			valueelement = [areacode,cityname,numdigits]
			valuescrawled.append(valueelement)
	return valuescrawled	
#create a csv file and add all values crawled

def convertToCSV(valuescrawled):
		valuescsv = csv.writer(open('values.csv', 'wb'), delimiter=',',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
		#go through each row and add to csv file
		for values in valuescrawled:
			valuescsv.writerow(values)
		


		
		


#get html of uk number home page
homepagehtml= getHtml()
#get all other urls needed to crawl
urlstocrawl = getLinkElements(homepagehtml)
#crawl all the urls and create list of values crawled
valuescrawled =  crawlURL(urlstocrawl)
#convert to csv
convertToCSV(valuescrawled)
print "Saved under values.csv"

