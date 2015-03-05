import urllib2
import requests

from config import DACHS_SERVERS, CHIVO_URL


#FILE_URL = "http://10.10.3.56:8080/getproduct/fitsdachs/res/FITS/" #Bender ip
#BENDER_URL = "http://alma-be.lirae.cl:8080"
BENDER_URL = "http://alma-be.lirae.cl:8080"
FILE_URL = BENDER_URL+"/getproduct/fitsdachs/res/"

SERVICEPARAMS = {
	"tap": "ivo://ivoa.net/std/TAP",
	"sia": "ivo://ivoa.net/std/SIA",
	"ssa": "ivo://ivoa.net/std/SSA",
	"scs": "ivo://ivoa.net/std/ConeSearch"
}
#Empty list
catalogsList= list()	


class CustomResponse():
	def __init__(self):
		self.text = None
		self.headers = None

#Has all the metadata from the catalog and make the different query's
class Catalog():
	def __init__(self, data):
		#All the metadata
		self.status = 'active'
		self.title = data["title"] if data.has_key("title") else None
		self.shortname = data["shortname"] if data.has_key("shortname") else None
		self.capabilities= data["capabilities"] if data.has_key("capabilities") else None
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
				return i['accessurl'].replace("?","")
		return False
	
	def replaceFilePath(self,r):
		res = CustomResponse()
		res.headers = r.headers
		res.text = r.text
		if self.filePath != None:
			text = r.text.replace(self.filePath, CHIVO_URL+"/"+self.shortname+"/file")
			res.text = text
		return res

	
	#Generic query, it calls the other query types.
	def query(self,parameters, method, queryType, route = None):
		#All services
		if method == "GET":	
			if queryType == "scs" :
				r=self.scsQuery(parameters)
				return self.replaceFilePath(r)
			elif queryType == "sia":
				if not("FORMAT" in parameters.keys()):
					parameters = dict(parameters)
					parameters["FORMAT"] = "ALL"
					
				r=self.siaQuery(parameters)
				return self.replaceFilePath(r)

			elif queryType == "ssa":
				r=self.ssaQuery(parameters)
				return self.replaceFilePath(r)
			else:
				return False
		#Only tap 
		else:
			return False	
		
		
	#SCS
	def scsQuery(self,parameters):
		r = requests.get(self.getAcessUrl("ConeSearch") , params = parameters)
		return r
	#SSA
	def ssaQuery(self, parameters):
		r = requests.get(self.getAcessUrl("SSA") , params = parameters)
		return r
	#SIA
	def siaQuery(self,parameters):
		#r = requests.get(self.getAcessUrl("SIA") , params = parameters, stream = True)
		r = requests.get(self.getAcessUrl("SIA"), params = parameters)
		return r
	
	#Tap
	
	##SyncQuery
	def tapSyncQuery(self, params):
		url = self.getAcessUrl("TAP")+"/sync"
		
		try:
			req = urllib2.Request(url, params)
			response = urllib2.urlopen(req)
			res = CustomResponse()
			res.text = response.read()
			res.headers = response.headers
			return self.replaceFilePath(res)
		except urllib2.HTTPError as e:
			error_message = e.read()
			return error_message
			
	##Async Simple Query
	def tapAsyncQuery(self, params, method):
		### If we get POST method, is a request with parameters
		if method == "POST":
			#Making the request then sending it, and getting a response
			req = urllib2.Request(self.getAcessUrl("TAP")+"/async", params)
			response = urllib2.urlopen(req)
			return response
		
		### If the method is get we should get all the ID's from the previous requests
		elif method == "GET":
			r = requests.get(self.getAcessUrl("TAP")+"/async")
			return r
			
	##Show tapAsyncJob info	
	def tapAsyncJob(self, jobId):
		r = requests.get(self.getAcessUrl("TAP")+"/async/"+jobId)
		return r
	##Show list of results
	def tapAsyncResults(self, jobId):
		r = requests.get(self.getAcessUrl("TAP")+"/async/"+jobId+"/results")
		return self.replaceFilePath(r)
	##Show result itself
	def tapAsyncResult(self,jobId, path):
		r = requests.get(self.getAcessUrl("TAP")+"/async/"+jobId+"/results/"+path)
		return r
	##Job Quote
	def tapAsyncQuote(self,jobId):
		r = requests.get(self.getAcessUrl("TAP")+"/async/"+jobId+"/quote")
		return r		
	##Execution duration
	def tapAsyncDuration(self,jobId):
		r = requests.get(self.getAcessUrl("TAP")+"/async/"+jobId+"/quote")
		return r		
	
	##Execution destruction
	def tapAsyncDestruction(self,jobId):
		r = requests.get(self.getAcessUrl("TAP")+"/async/"+jobId+"/destruction")
		return r
	##Return Tap tables	
	def tapTables(self):
		r = requests.get(self.getAcessUrl("TAP")+"/tables/")

		return r
	
	##Return Tap Capabilities
	def tapCapabilities(self):
		r = requests.get(self.getAcessUrl("TAP")+"/capabilities")
		return r
	
	##Return if the sistem is up or not
	def tapAvailability(self):
		r = requests.get(self.getAcessUrl("TAP")+"/availability")
		return r
	##Tap phase
	def tapPhase(self,jobID, method,params = None):
		if method == 'GET':
			r = requests.get(self.getAcessUrl("TAP")+"/async/"+jobId+"/phase")
			return r
		elif method == 'POST':
			req = urllib2.Request(self.getAcessUrl("TAP")+"/async/"+jobID+"/phase", params)
			response = urllib2.urlopen(req)
			return response
	
	##Alias for visible url
	def setAlias(self,data):
		self.alias = data
		return True
			
	def getAlias(self):
		if self.alias:
			return self.alias

		return False
	
	##Real filepath for the catalog	
	def setFilePath(self,path):
		self.filePath = path
		return True
	
	def filePath():
		if self.filePath():
			return self.filePath
		return False



#Generic Registry, list of catalogs, we need to implement keyword search and other stuff
class Registry():
	def __init__(self):
		self.catalogs = dict()
		return None
		
	def append(self, catalog):
		self.catalogs[catalog.shortname] = catalog
	
	def getCatalog(self , shortname):
		return self.catalogs[shortname]	if self.catalogs.has_key(shortname) else None
		

#Chivo Registry, now has only 1 test catalog, with testing metadata
class ChivoRegistry(Registry):
	def __init__(self):

		self.catalogs = dict()
		
		for catalog in DACHS_SERVERS:
			filePath = catalog['filePath'] if 'filepath' in catalog.keys() else None

			a = catalog['capabilities']

			_temp = []
			_alias = []
			for i in zip(a.keys(),a.values()):
				_temp.append({'standardid':SERVICEPARAMS[i[0]], 'accessurl':i[1]})
				_alias.append({'standardid':SERVICEPARAMS[i[0]], 'accessurl':CHIVO_URL+"/"+catalog['shortname']+"/"+i[0]+"?"})
					
			newCat = Catalog({'shortname':catalog['shortname'], 'title': catalog['title'],'capabilities':_temp})
			newCat.setFilePath(filePath)

			newCat.setAlias({'shortname':catalog['shortname'], 'title': catalog['title'],'capabilities':_alias})

			self.append(newCat)


