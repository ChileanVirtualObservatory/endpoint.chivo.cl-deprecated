import subprocess
import urllib
import urllib2
import requests
import json

from os import system
from flask import Flask, render_template, request, Response, redirect

returnType = 'text/xml'
MAX = 1000

#Catalog class, made once in the application and change the catalog in use in execution time
class Catalog:
	catalogsIvoa = dict()
	
	#Default came with "alma" catalog
	def __init__(self,catalog= None):
		self.getRegistry()
		self.catalogsIvoa["alma"] = {
		"capabilities":[
						{	
							"standardid": "ivo://ivoa.net/std/TAP",
							"accessurl" : "http://wfaudata.roe.ac.uk/twomass-dsa/TAP"
						}
						, 
						{
							"standardid":"ivo://ivoa.net/std/SCS",
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
			
		for item in catalogsList:
			if item.has_key('shortname'):
				self.catalogsIvoa[item['shortname']] = item

	#Change the object to another catalog
	def setCatalog(self,catalog):
		self.dic = self.catalogsIvoa[catalog]
		return None	
		
	#Return main catalog	
	def getCatalogsIvoa	(self):
		return self.catalogsIvoa
		
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
			if service.upper() in i['standardid']:
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
		r = requests.get(self.getAcessUrl("scs") , params = parameters, stream = True)
		return r
	#SSA
	def ssaQuery(self, parameters):
		r = requests.get(self.getAcessUrl("ssa") , params = parameters, stream = True)
		return r
	#SIA
	def siaQuery(self,parameters):
		r = requests.get(self.getAcessUrl("sia") , params = parameters, stream = True)
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
			
			r = requests.get(self.getAcessUrl("tap") + params , stream = True)
			
			return r

		elif method == "POST":
			if not "qid" in route.keys():
				data = query
				
				print self.getAcessUrl("tap")+"/"+route["option"]
				
                req = urllib2.Request(self.getAcessUrl("tap")+"/"+route["option"], data)
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

#Application Itself
app = Flask(__name__)
catalogIvoa = Catalog()



@app.route('/')
def index():
	return 'Index Page'

@app.route('/<catalog>')
def catalogServices(catalog):
	if catalog in catalogIvoa.getCatalogsIvoa().keys():
		catalogIvoa.setCatalog(catalog)
		return " ".join(catalogIvoa.getServices())
	else:
		return 'Catalog not found'

@app.route('/<catalog>/<queryType>', methods=['POST', 'GET'])
def query(catalog, queryType):
	print catalog
	print queryType
	try:
		catalogIvoa.setCatalog(catalog)
		if queryType in catalogIvoa.getServices():
			if request.method == "GET":
				r = catalogIvoa.query(request.args, request.method, queryType) 
				return Response(streamDataGet(r), mimetype= returnType)
			elif request.method == "POST" and queryType == "tap":
				r = catalogIvoa.query(urllib.urlencode(request.form), request.method, queryType)
				return Response(streamDataPost(r), mimetype= returnType)
			
		return 'Catalog without service'
	except Exception as e:
		raise
		return 'No catalog found ' + str(e)

@app.route('/<catalog>/tap')
def tap(catalog):
	catalogIvoa.setCatalog(catalog)
	if 'tap' in catalogIvoa.getServices():
		return 'OK'

@app.route('/<catalog>/tap/<path:route>', methods = ['GET', 'POST'])
def queryTap(catalog,route=None):
	catalogIvoa.setCatalog(catalog)
	route = map(str,route.split("/"))
	dictRoute = dict()
	if len(route) > 0:
		dictRoute["option"] = route[0]
	if len(route) > 1:
		dictRoute["qid"] = route[1]
	if len(route) > 2:
		dictRoute["qidOption"] = route[2]
	if len(route) > 3:
		dictRoute["qidOption"] = route[3]
	
	if len(route) > 4:
		return "Bad Tap Request"
	
	if 'tap' in catalogIvoa.getServices():
		
		if request.method == "GET":
				r = catalogIvoa.query(None, request.method, "tap" , dictRoute)
				return Response(streamDataGet(r), mimetype= returnType)
				
		elif request.method == "POST":
			print urllib.urlencode(request.form)
			print dictRoute
			r = catalogIvoa.query(urllib.urlencode(request.form), request.method, "tap",dictRoute)
			return Response(streamDataPost(r), mimetype= returnType)
	return 'Bad Tap Request1'

@app.route('/registry', methods = ['GET'])
def registry():
	
	#Max entries in registry page
	MAX = 100
	
	if request.args:
		page = int(request.args['page'])
	else:
		page = 1
	
	cat = dict()
	catalogs = catalogIvoa.getCatalogsIvoa()
	
	for i in catalogs:
		catalogIvoa.setCatalog(i)
		cat[i] =catalogIvoa.getServices()
	
	if len(cat.keys())%MAX != 0:
		pages =  (len(cat.keys())/MAX) + 1
	else:
		pages = len(cat.keys())/MAX
	
	keys = sorted(cat.keys())[(page-1)*MAX:page*MAX]
	return render_template('registry.html' , cat = cat, keys = keys, pages = pages, page = page, MAX = MAX)

if __name__ == '__main__':
    app.run(debug=True)
