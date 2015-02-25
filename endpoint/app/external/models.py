import urllib2
import requests
import json
import threading
import copy

#Empry catalogs list
catalogsList = list()

#Has all the metadata from the service
class ExtService():
	def __init__(self, data):
		#All the metadata
		self.status = data["status"] if data.has_key("status") else None
		self.publisher = data["publisher"] if data.has_key("publisher") else None
		self.updated = data["updated"] if data.has_key("updated") else None
		self.contentlevel = data["contentlevel"] if data.has_key("contentlevel") else None
		self.description = data["description"] if data.has_key("description") else None
		self.title = data["title"] if data.has_key("title") else None
		self.provenance = data["provenance"] if data.has_key("provenance") else None
		self.referenceurl = data["referenceurl"] if data.has_key("referenceurl") else None
		self.created = data["created"] if data.has_key("created") else None
		self.subjects = data["subjects"] if data.has_key("subjects") else None
		self.capabilities = data["capabilities"] if data.has_key("capabilities") else None
		self.contactname = data["contactname"] if data.has_key("contactname") else None
		self.shortname = data["shortname"] if data.has_key("shortname") else None
		self.identifier = data["identifier"] if data.has_key("identifier") else None
		self.type = data["type"] if data.has_key("type") else None
		self.data = data
		self.alias = None
	
	#Return the different protocols that are implemented in the catalog
	def getServices(self):
		serv = list()
		for i in self.capabilities:
			if "TAP" in i['standardid']:
				serv.append("tap")
			if "ConeSearch" in i['standardid']:
				serv.append("scs")
			if "SSA" in i['standardid']:
				serv.append("ssa")
			if "SIA" in i['standardid']:
				serv.append("sia")
		return serv
	
	#Get the url needed to make the query
	def getAcessUrl(self,service):
		catalogServices = self.capabilities
		for i in catalogServices:
			if service in i['standardid']:
				return i['accessurl']
		return False

#Generic Registry, list of catalogs, we need to implement keyword search and other stuff
class ExtRegistry():
	def __init__(self):
		self.catalogs = dict()
		return None
		
	def append(self, catalog):
		self.catalogs[catalog.shortname] = catalog
	
	def getCatalog(self , shortname):
		return self.catalogs[shortname]	if self.catalogs.has_key(shortname) else None
		
#VoParis Registry, we get the JSON for all the services, then merge them in a hash with Catalogs
class VOparisRegistry(ExtRegistry):
	def __init__(self):
		self.catalogs = dict()
		self.getRegistry()
	
	def getRegistry(self):
		
		#Max response items
		MAX = 1000

		#All standardid from ivoa services, those are the params from the query
		SERVICEPARAMS = {
			"tap":'standardid:"ivo://ivoa.net/std/TAP"',
			"sia": 'standardid:"ivo://ivoa.net/std/SIA"',
			"ssa": 'standardid:"ivo://ivoa.net/std/SSA"',
			"scs": 'standardid:"ivo://ivoa.net/std/ConeSearch"',
			}

		
		def threadQuery(serv):
			print "Starting "+ serv
			global catalogsList
			
			parameters ={"keywords": SERVICEPARAMS[serv] , "max": MAX}
			r = requests.get( "http://voparis-registry.obspm.fr/vo/ivoa/1/voresources/search", params = parameters)
			entries = json.loads(r.content)['resources']
			
			#Merging list and removing duplicated items
			catalogsList += entries
			catalogsList = {v['identifier']:v for v in catalogsList}.values()
			print "Ready "+serv
			
			print _type + " Ready"
		
		
		#We get all services with tap,sia,ssa,tap from vo-paris registry 
		for _type in SERVICEPARAMS:
			threadQuery(_type)
					
		#giving the catalogs to the external dictionary
		for item in catalogsList:
			if item.has_key('shortname'):
				self.catalogs[item['shortname']] = ExtService(item)
