import urllib

from classes import *
from func import *

from os import system
from flask import Flask, render_template, request, Response, redirect


#Application Itself
app = Flask(__name__)
chivoReg = ChivoRegistry()
extReg = VOparisRegistry() 

#Remove trailing slash in POST requests
@app.before_request
def remove_trailing_slash():
	if request.path != '/' and request.path.endswith('/') and request.method == "POST":
		return redirect(request.path[:-1], code=307)

#Index Page
@app.route('/')
def index():
	return 'Index Page'

#Renders MAX catalogs from alma's registry
@app.route('/registry/', methods = ['GET'])
def registry(Reg = chivoReg, external = None):
	
	#Max entries in registry page
	MAX = 100
	
	keys= list()
	
	#The page we are now
	if request.args:
		page = int(request.args['page'])
	else:
		page = 1
	
	#Getting catalog services
	cat = dict()
	for i in Reg.catalogs.keys():
		cat[i] =Reg.getCatalog(i).getServices()
	
	#Getting number of pages
	if len(cat.keys())%MAX != 0:
		pages =  (len(cat.keys())/MAX) + 1
	else:
		pages = len(cat.keys())/MAX
	
	for i in sorted(cat.keys())[(page-1)*MAX:page*MAX]:
		keys.append((i ,i))

	return render_template('registry.html' , cat = cat, keys = keys, pages = pages, page = page, MAX = MAX, external = external)

#External Registry
@app.route('/external/registry/', methods = ['GET'])
def extRegistry():
	return registry(extReg, True)

#Tap Catalog
@app.route('/<path:catalog>/tap/')
@app.route('/<path:catalog>/TAP/')
def tap(catalog, Reg = chivoReg):
	cat = Reg.getCatalog(catalog)
	if cat is None:
		return 'Error'
	if 'tap' in cat.getServices():
		return 'OK'

#Tap Sync Query, only POST method
@app.route('/<path:catalog>/tap/sync', methods = ['POST'])
def syncTap(catalog, Reg = chivoReg):
	data = urllib.urlencode(request.form)
	cat = Reg.getCatalog(catalog)
	#If the catalog is not in our registry
	if cat is None:
		return 'Error'
	#If the catalog has 'tap' service, we make the request
	if 'tap' in cat.getServices():
		res = cat.tapSyncQuery(data)
		return Response(streamDataPost(res) , mimetype=getResponseType(res.headers))
	return 'Error2'

#External Tap Sync Query
@app.route('/external/<path:catalog>/tap/sync', methods = ['POST'])
def extSyncTap(catalog):
	return syncTap(catalog, extReg)

#Show tap tables from a catalog
@app.route('/<path:catalog>/tap/tables/')
def tapTables(catalog, Reg= chivoReg):
	cat = Reg.getCatalog(catalog)
	#Validate catalog
	if cat is None:
		return 'Error'
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapTables()
		return Response(streamDataGet(r), mimetype=getResponseType(r.headers))

#Show tap capabilities from a catalog
@app.route('/<path:catalog>/tap/capabilities/')
def tapCapability(catalog, Reg= chivoReg):
	cat = Reg.getCatalog(catalog)
	#Validate catalog
	if cat is None:
		return 'Error'
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapCapabilities()
		return Response(streamDataGet(r), mimetype=getResponseType(r.headers))

#Show tap availability from a catalog		
@app.route('/<path:catalog>/tap/availability/')
def tapAvailability(catalog, Reg= chivoReg):
	cat = Reg.getCatalog(catalog)
	#Validate catalog
	if cat is None:
		return 'Error'
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapAvailability()
		return Response(streamDataGet(r), mimetype=getResponseType(r.headers))
		
#Tap Async Query, Post method for making request, and Get for getting all requests made
@app.route('/<path:catalog>/tap/async', methods=['POST', 'GET'])
def tapAsync(catalog, Reg= chivoReg):
	data = urllib.urlencode(request.form)
	cat = Reg.getCatalog(catalog)
	#If the catalog is not in our registry
	if cat is None:
		return 'Error'
	#If the catalog has 'tap' service, we make the request
	if 'tap' in cat.getServices():
		r = cat.tapAsyncQuery(data,request.method)
		print r.content
		if request.method == "POST":
			return Response(streamDataPost(r) , mimetype=getResponseType(r.headers))
		else:
			print r
			return Response(streamDataGet(r), mimetype=getResponseType(r.headers))		
		
#Tap Async Job Info
@app.route('/<path:catalog>/tap/async/<jobId>/', methods=['GET'])
@app.route('/<path:catalog>/TAP/async/<jobId>/', methods=['GET'])
def tapAsyncJob(catalog, jobId , Reg = chivoReg):
	cat = Reg.getCatalog(catalog)
	#Validate catalog
	if cat is None:
		return 'Error'
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapAsyncJob(jobId)
		return Response(streamDataGet(r), mimetype=getResponseType(r.headers))



@app.route('/<path:catalog>/tap/async/<jobId>/results', methods=['GET'])
@app.route('/<path:catalog>/TAP/async/<jobId>/results', methods=['GET'])
def tapAsyncJob(catalog, jobId , Reg = chivoReg):
	cat = Reg.getCatalog(catalog)
	#Validate catalog
	if cat is None:
		return 'Error'
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapAsyncResults(jobId)
		return Response(streamDataGet(r), mimetype=getResponseType(r.headers))
		
		
@app.route('/<path:catalog>/tap/async/<jobId>/results/<path:result>', methods=['GET'])
@app.route('/<path:catalog>/TAP/async/<jobId>/results/<path:result>', methods=['GET'])
def tapAsyncJob(catalog, jobId, result, Reg = chivoReg):
	cat = Reg.getCatalog(catalog)
	#Validate catalog
	if cat is None:
		return 'Error'
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapAsyncResult(jobId,result)
		return Response(streamDataGet(r), mimetype=getResponseType(r.headers))

@app.route('/<path:catalog>/tap/async/<jobId>/quote', methods=['GET'])
@app.route('/<path:catalog>/TAP/async/<jobId>/quote', methods=['GET'])
def tapAsyncJob(catalog, jobId , Reg = chivoReg):
	cat = Reg.getCatalog(catalog)
	#Validate catalog
	if cat is None:
		return 'Error'
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapAsyncQuote(jobId)
		return Response(streamDataGet(r), mimetype=getResponseType(r.headers))
		

#Show external tap tables from a catalog
@app.route('/external/<path:catalog>/tap/tables')
def extTapTables(catalog):
	return tapTables(catalog, Reg= extReg)

#External TAP
@app.route('/external/<path:catalog>/tap/')
@app.route('/external/<path:catalog>/TAP/')
def ExternTap(catalog):
	return tap(catalog, extReg)

#Make SIA Query
@app.route('/<path:catalog>/sia/', methods=['POST', 'GET'])
@app.route('/<path:catalog>/SIA/', methods=['POST', 'GET'])
def sia(catalog, Reg = chivoReg):
	
	queryType = "sia"
	cat = Reg.getCatalog(catalog)
	#Validate catalog
	if cat is None:
		return 'Error'
	#Validate SIA service
	if queryType in cat.getServices():
		#Protocol need GET
		if request.method == "GET":
			#Making the request			
			r = cat.query(request.args, request.method, queryType) 
			if request.args:
				return Response(streamDataGet(r), mimetype= getResponseType(r.headers))
			 
			return Response(streamDataGet(r))		
	return 'Catalog without service'
	
@app.route('/external/<path:catalog>/sia', methods=['POST', 'GET'])
@app.route('/external/<path:catalog>/SIA', methods=['POST', 'GET'])
def ExternSia(catalog):
	return sia(catalog, extReg)

#SCS query
@app.route('/<path:catalog>/scs', methods=['POST', 'GET'])
@app.route('/<path:catalog>/SCS', methods=['POST', 'GET'])
def scs(catalog, Reg= chivoReg):
	queryType = "scs"
	cat = Reg.getCatalog(catalog)
	#validating catalog
	if cat is None:
		return 'Error'
	#validating service
	if queryType in cat.getServices():
		# GET needed in protocol
		if request.method == "GET":
			#Making Query
			r = cat.query(request.args, request.method, queryType ) 
			if request.args:
				return Response(streamDataGet(r), mimetype= getResponseType(r.headers))
			
			return Response(streamDataGet(r))
	return 'Catalog without service'

@app.route('/external/<path:catalog>/scs/', methods=['POST', 'GET'])
@app.route('/external/<path:catalog>/SCS/', methods=['POST', 'GET'])
def ExternScs(catalog):
	return scs(catalog, extReg)

#SSA Query
@app.route('/<path:catalog>/ssa/', methods=['POST', 'GET'])
@app.route('/<path:catalog>/SSA/', methods=['POST', 'GET'])
def ssa(catalog, Reg = chivoReg):
	
	queryType = "ssa"
	cat = Reg.getCatalog(catalog)
	#validating catalog
	if cat is None:
		return 'Error'
	#validating service
	if queryType in cat.getServices():
		#GET needed in protocol
		if request.method == "GET":
			#Making request
			r = cat.query(request.args, request.method, queryType) 
			if request.args:
				return Response(streamDataGet(r), mimetype= getResponseType(r.headers))
			
			return Response(streamDataGet(r))
			
	return 'Catalog without service'
	
@app.route('/external/<path:catalog>/ssa/', methods=['POST', 'GET'])
@app.route('/external/<path:catalog>/SSA/', methods=['POST', 'GET'])
def ExternSsa(catalog):
	return ssa(catalog, extReg)

#Showing catalog metadata
@app.route('/<path:catalog>/')
def catalogServices(catalog, Reg = chivoReg):
	if catalog in Reg.catalogs.keys():
		i =Reg.getCatalog(catalog)
		return " ".join(i.getServices())
	return 'Catalog not found'
	
@app.route('/external/<path:catalog>/')
def exterCatalog(catalog):
	return catalogServices(catalog, extReg)

@app.route('/raise/')
def Praise():
	raise
	return	
	
if __name__ == '__main__':
    app.run(debug=True)
