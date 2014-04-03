import subprocess
import urllib
import urllib2
import requests
import json

CHIVO_CATALOG = 0
EXTERNAL_CATALOG = 1 
MAX = 1000

#Catalog class, made once in the application and change the catalog in use in execution time
class Catalog:
	catalogsChivo = dict()
	externalCatalog = dict()
	
	#Default came with "alma" catalog
	def __init__(self,catalog= None):
		
		self.getRegistry()
		
		self.catalogsChivo["alma"] = {
		u'capabilities':[
						{	
							"standardid": "ivo://ivoa.net/std/TAP",
							"accessurl" : "http://wfaudata.roe.ac.uk/twomass-dsa/TAP"
						}
						, 
						{
							"standardid":"ivo://ivoa.net/std/ConeSearch",
							"accessurl" : "http://wfaudata.roe.ac.uk/twomass-dsa/DirectCone?DSACAT=TWOMASS&DSATAB=twomass_psc"
						}
						,
						{
							"standardid": "ivo://ivoa.net/std/SSA" ,
							"accessurl" : "http://wfaudata.roe.ac.uk/6dF-ssap/?" 
						}
						,
						{
							"standardid":"ivo://ivoa.net/std/SIA" ,
							"accessurl" :"http://irsa.ipac.caltech.edu/ibe/sia/wise/prelim/p3am_cdd?"
						}
					]
		}
			
	
	#Initate Main dicctionary with voparis registry	
	def getRegistry(self):
		#All standardid from ivoa services
		SERVICEPARAMS = {
			"tap":'standardid:"ivo://ivoa.net/std/TAP"',
			"sia": 'standardid:"ivo://ivoa.net/std/SIA"',
			"ssa": 'standardid:"ivo://ivoa.net/std/SSA"',
			"scs": 'standardid:"ivo://ivoa.net/std/ConeSearch"',
			}
		
		catalogsList= list()
		
		#We get all services with tap,sia,ssa,tap from vo-paris registry 
		for _type in SERVICEPARAMS:
			parameters ={"keywords": SERVICEPARAMS[_type] , "max": MAX}
			r = requests.get( "http://voparis-registry.obspm.fr/vo/ivoa/1/voresources/search", params = parameters)
			entries = json.loads(r.content)['resources']
			
			#Merging list and removing duplicated items
			catalogsList += entries
			catalogsList = {v['identifier']:v for v in catalogsList}.values()
			
			print _type + " Ready"
		
		#giving the catalogs to the external dictionary
		for item in catalogsList:
			if item.has_key('shortname'):
				self.externalCatalog[item['shortname']] = item

	#Change the object to another catalog
	def setCatalog(self,catalog):
		if catalog in self.catalogsChivo.keys():
			self.dic = self.catalogsChivo[catalog]
			return CHIVO_CATALOG
		elif catalog in self.externalCatalog.keys():
			self.dic = self.externalCatalog[catalog]
			return EXTERNAL_CATALOG
		return None	
		
	#Return main catalog	
	def getcatalogsChivo	(self):
		return self.catalogsChivo
		
	#Get the services from the catalog in use
	def getServices(self):
		serv = list()
		catalogServices = self.dic['capabilities']
		for i in catalogServices:
			if "TAP" in i['standardid']:
				serv.append("tap")
			if "ConeSearch" in i['standardid']:
				serv.append("scs")
			if "SSA" in i['standardid']:
				serv.append("ssa")
			if "SIA" in i['standardid']:
				serv.append("sia")
		return serv	
		
	#Get the acces url from the catalog in use
	def getAcessUrl(self,service):
		catalogServices = self.dic['capabilities']
		for i in catalogServices:
			if service in i['standardid']:
				return i['accessurl']
		return False
		
	#Generic query, it calls the other query types.
	def query(self,parameters, method, queryType, route = None):
		#All services
		if method == "GET":	
			if queryType == "scs" :
				r=self.scsQuery(parameters)
				return r
			elif queryType == "sia":
				r=self.siaQuery(parameters)
				return r

			elif queryType == "ssa":
				r=self.ssaQuery(parameters)
				return r
			elif queryType == "tap":
				r = self.tapQuery(parameters, method, route)
				return r
			else:
				return False
		#Only tap 
		elif method == "POST" and queryType == "tap":
			r=self.tapQuery(parameters, method, route)
			return r
		else:
			return False

	#SCS
	def scsQuery(self,parameters):
		r = requests.get(self.getAcessUrl("ConeSearch") , params = parameters, stream = True)
		return r
	#SSA
	def ssaQuery(self, parameters):
		r = requests.get(self.getAcessUrl("SSA") , params = parameters, stream = True)
		return r
	#SIA
	def siaQuery(self,parameters):
		r = requests.get(self.getAcessUrl("SIA") , params = parameters, stream = True)
		return r
	#TAP
	def tapQuery(self, query , method , route):
		
		if method == "GET":
			params  = "/" + route["option"]
			if "qid" in route.keys():
					params += "/" + route["qid"]
			if "qidOption" in route.keys():
					params += "/" + route["qidOption"]
			if "qidOptionRequest" in route.keys():
					params += "/" + route["qidOptionRequest"]
			
			r = requests.get(self.getAcessUrl("TAP") + params , stream = True)
			
			return r

		elif method == "POST":
			if not "qid" in route.keys():
				data = route
                req = urllib2.Request(self.getAcessUrl("TAP")+"/"+route["option"], data)
                response = urllib2.urlopen(req)
                return response	
		return False

#Functions for data streaming
def streamDataGet(r):
	for line in r.iter_lines():
			if line: # filter out keep-alive new lines
				yield line

def streamDataPost(r):
	CHUNK = 1024
	for the_page in iter(lambda: r.read(CHUNK), ''):
		yield the_page

def getResponseType(content):
	if "content-type" in content.keys():
		return content["content-type"].split(";")[0]
	else:
		return 'text/xml'

