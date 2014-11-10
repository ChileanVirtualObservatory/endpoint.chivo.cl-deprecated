import urllib

from classes import *
from func import *
#~ from name_resolver import *

from os import system
from flask import Flask, render_template, request, Response, redirect
#~ from celery.schedules import crontab
#~ from tasks import update_external

#Application Itself
app = Flask(__name__)
chivoReg = ChivoRegistry()
extReg = VOparisRegistry() 
#~ chivoBib = ChivoBib()

#Cron celery configuration to update
#external from voparis registry
#~ CELERYBEAT_SCHEDULE = {
	#~ 'update-catalogs': {
	#~ 'task': 'tasks.update_external', 
	#~ 'schedule': crontab(hour='*/1'),
	#~ 'args':(extReg,),
	#~ },
#~ }

#Remove trailing slash in POST requests
@app.before_request
def remove_trailing_slash():
	if request.path != '/' and request.path.endswith('/') and request.method == "POST":
		return redirect(request.path[:-1], code=307)

#Index Page
@app.route('/')
def index():
	return render_template("index.html")
	
#Renders MAX catalogs from alma's registry
@app.route('/registry/', methods = ['GET'])
def registry(Reg = chivoReg):
	
	cat = []
	for i in Reg.catalogs.keys():
		cati=Reg.getCatalog(i)
		if cati.status == "active":
			_temp = dict()
			_temp["shortname"] = cati.shortname
			_temp["title"] = cati.title
			_temp["capabilities"] = cati.capabilities
			cat.append(_temp)
	
	return json.dumps(cat)
	
@app.route('/registry/allTap', methods = ['GET'])
@app.route('/tap' , methods = ['GET'])
def registry1(Reg = chivoReg,  service = "tap"):
	SERVICEPARAMS = {
			"tap": "ivo://ivoa.net/std/TAP",
			"sia": "ivo://ivoa.net/std/SIA",
			"ssa": "ivo://ivoa.net/std/SSA",
			"scs": "ivo://ivoa.net/std/ConeSearch",
			}
	cat = []
	for i in Reg.catalogs.keys():
		cati=Reg.getCatalog(i)
		if cati.status == "active" and service in cati.getServices() :
			_temp = dict()
			_temp["title"] =cati.title
			_temp["shortname"] = cati.shortname
			unfiltered = cati.capabilities
			for s in unfiltered:
				if s["standardid"] == SERVICEPARAMS[service]:
					_temp["accessurl"] = s["accessurl"]
			cat.append(_temp)
	return json.dumps(cat)
	
@app.route('/registry/allScs', methods = ['GET'])
@app.route('/scs' , methods = ['GET'])
def registry2():
	return registry1(chivoReg, "scs")

@app.route('/registry/allSia', methods = ['GET'])
@app.route('/sia' , methods = ['GET'])
def registry3():
	return registry1(chivoReg, "sia")
	
@app.route('/registry/allSsa', methods = ['GET'])
@app.route('/ssa' , methods = ['GET'])
def registry4():
	return registry1(chivoReg, "ssa")
	
	
@app.route('/external/registry/allTap', methods = ['GET'])
@app.route('/external/tap', methods = ['GET'])
def extRegistry1():
	internal = json.loads(registry1(chivoReg, "tap"))
	external = json.loads(registry1(extReg ,"tap"))
	return json.dumps(internal+external)
	
	
@app.route('/external/registry/allScs', methods = ['GET'])
@app.route('/external/scs', methods = ['GET'])
def extRegistry2():
	internal = json.loads(registry1(chivoReg, "scs"))
	external = json.loads(registry1(extReg ,"scs"))
	return json.dumps(internal+external)

@app.route('/external/registry/allSia', methods = ['GET'])
@app.route('/external/sia', methods = ['GET'])
def extRegistry3():
	internal = json.loads(registry1(chivoReg, "sia"))
	external = json.loads(registry1(extReg ,"sia"))
	return json.dumps(internal+external)
	
@app.route('/external/registry/allSsa', methods = ['GET'])
@app.route('/external/ssa', methods = ['GET'])
def extRegistry4():
	external = json.loads(registry1(extReg ,"ssa"))
	return json.dumps(external)
	
#External Registry
@app.route('/external/registry/', methods = ['GET'])
def extRegistry():
	internal = json.loads(registry(chivoReg))
	external = json.loads(registry(extReg))
	return json.dumps(internal+external)

#Tap Catalog
@app.route('/<catalog>/tap/')
@app.route('/<catalog>/TAP/')
def tap(catalog, Reg = chivoReg):
	cat = Reg.getCatalog(catalog)
	if cat is None:
		return 'Error'
	if 'tap' in cat.getServices():
		return 'OK'

#Tap Sync Query, only POST method
@app.route('/<catalog>/tap/sync', methods = ['POST'])
def syncTap(catalog, Reg = chivoReg):
	data = urllib.urlencode(request.form)
	cat = Reg.getCatalog(catalog)
	#If the catalog is not in our registry
	if cat is None:
		return 'Error'
	#If the catalog has 'tap' service, we make the request
	if 'tap' in cat.getServices():
		
		res = cat.tapSyncQuery(data)
		if type(res) is str:
			return res
		return Response(streamDataPost(res) , mimetype=getResponseType(res.headers))
	return 'Error2'

#~ #External Tap Sync Query
#~ @app.route('/external/<path:catalog>/tap/sync', methods = ['POST'])
#~ def extSyncTap(catalog):
	#~ return syncTap(catalog, extReg)

#Show tap tables from a catalog
@app.route('/<catalog>/tap/tables/')
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
@app.route('/<catalog>/tap/capabilities/')
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
@app.route('/<catalog>/tap/availability/')
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
@app.route('/<catalog>/tap/async', methods=['POST', 'GET'])
def tapAsync(catalog, Reg= chivoReg):
	data = urllib.urlencode(request.form)
	cat = Reg.getCatalog(catalog)
	#If the catalog is not in our registry
	if cat is None:
		return 'Error'
	#If the catalog has 'tap' service, we make the request
	if 'tap' in cat.getServices():
		r = cat.tapAsyncQuery(data,request.method)
		if request.method == "POST":
			return Response(streamDataPost(r) , mimetype=getResponseType(r.headers))
		else:
			return Response(streamDataGet(r), mimetype=getResponseType(r.headers))		
		
#Tap Async Job Info
@app.route('/<catalog>/tap/async/<jobId>/', methods=['GET'])
@app.route('/<catalog>/TAP/async/<jobId>/', methods=['GET'])
def tapAsyncJob(catalog, jobId , Reg = chivoReg):
	cat = Reg.getCatalog(catalog)
	#Validate catalog
	if cat is None:
		return 'Error'
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapAsyncJob(jobId)
		return Response(streamDataGet(r), mimetype=getResponseType(r.headers))



@app.route('/<catalog>/tap/async/<jobId>/results/', methods=['GET'])
@app.route('/<catalog>/TAP/async/<jobId>/results/', methods=['GET'])
def tapAsyncResults(catalog, jobId , Reg = chivoReg):
	cat = Reg.getCatalog(catalog)
	#Validate catalog
	if cat is None:
		return 'Error'
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapAsyncResults(jobId)
		return Response(streamDataGet(r), mimetype=getResponseType(r.headers))

@app.route('/<catalog>/tap/async/<jobId>/results/<path:result>', methods=['GET'])
@app.route('/<catalog>/TAP/async/<jobId>/results/<path:result>', methods=['GET'])
def tapAsyncResult(catalog, jobId, result, Reg = chivoReg):
	cat = Reg.getCatalog(catalog)
	#Validate catalog
	if cat is None:
		return 'Error'
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapAsyncResult(jobId,result)
		return Response(streamDataGet(r), mimetype=getResponseType(r.headers))

@app.route('/<catalog>/tap/async/<jobId>/quote/', methods=['GET'])
@app.route('/<catalog>/TAP/async/<jobId>/quote/', methods=['GET'])
def tapAsyncQuote(catalog, jobId , Reg = chivoReg):
	cat = Reg.getCatalog(catalog)
	#Validate catalog
	if cat is None:
		return 'Error'
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapAsyncQuote(jobId)
		return Response(streamDataGet(r), mimetype=getResponseType(r.headers))
		
@app.route('/<catalog>/tap/async/<jobId>/destruction/', methods=['GET'])
@app.route('/<catalog>/TAP/async/<jobId>/destruction/', methods=['GET'])
def tapAsyncDestruction(catalog, jobId , Reg = chivoReg):
	cat = Reg.getCatalog(catalog)
	#Validate catalog
	if cat is None:
		return 'Error'
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapAsyncDestruction(jobId)
		return Response(streamDataGet(r), mimetype=getResponseType(r.headers))		
		
@app.route('/<catalog>/tap/async/<jobId>/executionduration/', methods=['GET'])
@app.route('/<catalog>/TAP/async/<jobId>/executionduration/', methods=['GET'])
def tapAsyncDuration(catalog, jobId , Reg = chivoReg):
	cat = Reg.getCatalog(catalog)
	#Validate catalog
	if cat is None:
		return 'Error'
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapAsyncDuration(jobId)
		return Response(streamDataGet(r), mimetype=getResponseType(r.headers))

@app.route('/<catalog>/tap/async/<jobId>/phase/', methods= ['GET', 'POST'])
@app.route('/<catalog>/TAP/async/<jobId>/phase/', methods= ['GET', 'POST'])
def tapAsyncPhase(catalog, jobID, Reg = chivoReg):
	cat = Reg.getCatalog(catalog)
	data = urllib.urlencode(request.form)
	#Validate catalog
	if cat is None:
		return 'Error'
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapAsyncPhase(jobId, request.method, data)
		if request.method == "GET":
			return Response(streamDataGet(r), mimetype=getResponseType(r.headers))
		elif request.method == 'POST':
			return Response(streamDataPost(r), mimetype=getResponseType(r.headers))

#Make SIA Query
@app.route('/<catalog>/sia', methods=['POST', 'GET'])
@app.route('/<catalog>/SIA', methods=['POST', 'GET'])
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
	

#SCS query
@app.route('/<catalog>/scs', methods=['POST', 'GET'])
@app.route('/<catalog>/SCS', methods=['POST', 'GET'])
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

#SSA Query
@app.route('/<catalog>/ssa', methods=['POST', 'GET'])
@app.route('/<catalog>/SSA', methods=['POST', 'GET'])
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

#Showing catalog metadata
@app.route('/<catalog>/')
def catalogServices(catalog, Reg = chivoReg):
	if catalog in Reg.catalogs.keys():
		i =Reg.getCatalog(catalog)
		return " ".join(i.getServices())
	return 'Catalog not found'
	
	
	
#Chivo Bib Conesearch
@app.route('/bib/conesearch', methods=['GET'])
def bibConesearch():
	params = request.args
	ra = float(params["RA"])
	dec = float(params["DEC"])
	sr = float(params["SR"])
	votable = chivoBib.scs(ra,dec,sr)
	return Response(votable, mimetype = "text/xml")
#Chivo Name Resolver
@app.route('/name_resolver/<name>', methods=['GET'])
def name_resolver(name):
	response = chivoBib.nameResolver(name)
	return Response(response, mimetype = "application/json")

	
if __name__ == '__main__':
	app.run(debug=True)
