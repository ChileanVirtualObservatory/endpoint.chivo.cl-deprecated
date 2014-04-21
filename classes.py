import urllib2
import requests
import json

#Has all the metadata from the catalog and make the different query's
class Catalog():
	def __init__(self, data):
		#All the metadata
		self.stauts = data["status"] if data.has_key("status") else None
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
	
	#~ #TAP
	#~ def tapQuery(self, query , method , route):
		#~ 
		#~ if method == "GET":
			#~ params  = "/" + route["option"]
			#~ if "qid" in route.keys():
					#~ params += "/" + route["qid"]
			#~ if "qidOption" in route.keys():
					#~ params += "/" + route["qidOption"]
			#~ if "qidOptionRequest" in route.keys():
					#~ params += "/" + route["qidOptionRequest"]
			#~ 
			#~ r = requests.get(self.getAcessUrl("TAP") + params , stream = True)
			#~ 
			#~ return r
#~ 
		#~ elif method == "POST":
			#~ if not "qid" in route.keys():
				#~ data = None
                #~ req = urllib2.Request(self.getAcessUrl("TAP")+"/"+route["option"], data)
                #~ response = urllib2.urlopen(req)
                #~ return response	
		#~ return False
		#~ 


#Generic Registry, list of catalogs, we need to implement keyword search and other stuff
class Registry():
	def __init__(self):
		self.catalogs = dict()
		return None
		
	def append(self, catalog):
		self.catalogs[catalog.shortname] = catalog
	
	def getCatalog(self , shortname):
		return self.catalogs[shortname]	
		

#Chivo Registry, now has only 1 test catalog, with testing metadata
class ChivoRegistry(Registry):
	def __init__(self):
		self.catalogs = dict()
		alma = Catalog(
		{
				u'status' : "active",
				
				u'publisher': 'LIRAE',
				
				u'updated' : '2013-04-04T02:00:00.000Z',
				
				u'contentlevel': 'Research',
				
				u'description': 'Alma dataset',
				
				u'title': 'title',
				
				u'provenance': 'ivo://jvo/publishingregistry',
				
				u'referenceurl' : 'http://www.chivo.cl',
				
				u'created' : u'2013-01-18T08:37:52.000Z',
				
				u'subjects' :[u'ACTIVE GALACTIC NUCLEI', u'BLACK HOLES', u'QUASARS'],
				
				u'contactname' : 'Contact',
				
				u'shortname' : 'alma',
				
				u'identifier': 'identfier',
				
				u'type' : 'CatalogService',
				
				u'capabilities':[
							{	
								"standardid": "ivo://ivoa.net/std/TAP",
								"accessurl" : "http://wfaudata.roe.ac.uk/twomass-dsa/TAP"
							}
							, 
							{
								"standardid":"ivo://ivoa.net/std/ConeSearch",
								"accessurl" : "http://heasarc.gsfc.nasa.gov/xamin/vo/cone?showoffsets&table=atlascscpt&"
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
			)
		self.append(alma)


class VOparisRegistry(Registry):
	def __init__(self):
		self.catalogs = dict()
		self.__getRegistry()
		
	def __getRegistry(self):
		
		#Max response items
		MAX = 1000
		
		#All standardid from ivoa services
		SERVICEPARAMS = {
			#"tap":'standardid:"ivo://ivoa.net/std/TAP"',
			#"sia": 'standardid:"ivo://ivoa.net/std/SIA"',
			#"ssa": 'standardid:"ivo://ivoa.net/std/SSA"',
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
				self.catalogs[item['shortname']] = Catalog(item)
