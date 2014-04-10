from catalog import *

from os import system
from flask import Flask, render_template, request, Response, redirect

#Application Itself
app = Flask(__name__)
catalogIvoa = Catalog()

@app.route('/')
def index():
	return 'Index Page'

@app.route('/registry', methods = ['GET'])
def registry(external=None):
	
	#Max entries in registry page
	MAX = 100
	
	keys= list()
	
	if request.args:
		page = int(request.args['page'])
	else:
		page = 1
	
	cat = dict()
	if external == None:
		catalogs = catalogIvoa.getcatalogsChivo()
	elif external == 'external':
		catalogs = catalogIvoa.externalCatalog
	else:
		return None
	for i in catalogs:
		catalogIvoa.setCatalog(i)
		cat[i] =catalogIvoa.getServices()
	
	if len(cat.keys())%MAX != 0:
		pages =  (len(cat.keys())/MAX) + 1
	else:
		pages = len(cat.keys())/MAX
	
	for i in sorted(cat.keys())[(page-1)*MAX:page*MAX]:
		keys.append( (i, urllib.quote(i,'')))
		
	return render_template('registry.html' , cat = cat, keys = keys, pages = pages, page = page, MAX = MAX, external = external)

@app.route('/external/registry', methods = ['GET'])
def extRegs():
	return registry("external")

@app.route('/<path:catalog>')
@app.route('/<path:catalog>/')
def catalogServices(catalog, internal = True):
	if internal:
		if catalog in catalogIvoa.getcatalogsChivo().keys():
			i =catalogIvoa.setCatalog(catalog)
			if i == CHIVO_CATALOG:
				return " ".join(catalogIvoa.getServices())
	if internal == False:
		if catalog in catalogIvoa.externalCatalog.keys():
			i =catalogIvoa.setCatalog(catalog)
			if i== EXTERNAL_CATALOG:
				return " ".join(catalogIvoa.getServices())
	return 'Catalog not found'
	
@app.route('/external/<path:catalog>')
@app.route('/external/<path:catalog>/')
def exterCatalog(catalog):
	return catalogServices(catalog, False)
	


@app.route('/<path:catalog>/sia', methods=['POST', 'GET'])
@app.route('/<path:catalog>/SIA', methods=['POST', 'GET'])
def InternSia(catalog):
	int_ext = catalogIvoa.setCatalog(catalog)
	if int_ext == CHIVO_CATALOG:
		return sia(catalog)
	else: 
		return 'Error'
		
def sia(catalog):
	
	queryType = "sia"
	catalog = urllib.quote(catalog)

	try:
		catalogIvoa.setCatalog(catalog)
		if queryType in catalogIvoa.getServices():
			if request.method == "GET":
				
				r = catalogIvoa.query(request.args, request.method, queryType) 
				if request.args:
					return Response(streamDataGet(r), mimetype= getResponseType(r.headers))
				 
				return Response(streamDataGet(r))
	except:
		return 'Catalog without service'
			
	return 'Catalog without service'
	
@app.route('/external/<path:catalog>/sia', methods=['POST', 'GET'])
@app.route('/external/<path:catalog>/SIA', methods=['POST', 'GET'])
def ExternSia(catalog):
	int_ext = catalogIvoa.setCatalog(catalog)
	if int_ext == EXTERNAL_CATALOG:
		return sia(catalog)
	else: 
		return 'Error'

@app.route('/<path:catalog>/scs', methods=['POST', 'GET'])
@app.route('/<path:catalog>/SCS', methods=['POST', 'GET'])
def InternScs(catalog):
	int_ext = catalogIvoa.setCatalog(catalog)
	if int_ext == CHIVO_CATALOG:
		return scs(catalog)
	else: 
		return 'Error'
		
def scs(catalog):
	
	queryType = "scs"
	catalog = urllib.quote(catalog)

	try:
		catalogIvoa.setCatalog(catalog)
		if queryType in catalogIvoa.getServices():
			if request.method == "GET":
				
				r = catalogIvoa.query(request.args, request.method, queryType ) 
				if request.args:
					return Response(streamDataGet(r), mimetype= getResponseType(r.headers))
				
				return Response(streamDataGet(r))
	except:
		return 'Catalog without service'
			
	return 'Catalog without service'

@app.route('/external/<path:catalog>/scs', methods=['POST', 'GET'])
@app.route('/external/<path:catalog>/SCS', methods=['POST', 'GET'])
def ExternScs(catalog):
	int_ext = catalogIvoa.setCatalog(catalog)
	if int_ext == EXTERNAL_CATALOG:
		return scs(catalog)
	else: 
		return 'Error'

@app.route('/<path:catalog>/ssa', methods=['POST', 'GET'])
@app.route('/<path:catalog>/SSA', methods=['POST', 'GET'])
def InternSsa(catalog):
	int_ext = catalogIvoa.setCatalog(catalog)
	if int_ext == CHIVO_CATALOG:
		return ssa(catalog)
	else: 
		return 'Error'
		
def ssa(catalog):
	
	queryType = "ssa"
	catalog = urllib.quote(catalog)

	try:
		catalogIvoa.setCatalog(catalog)
		if queryType in catalogIvoa.getServices():
			if request.method == "GET":
				
				r = catalogIvoa.query(request.args, request.method, queryType) 
				if request.args:
					return Response(streamDataGet(r), mimetype= getResponseType(r.headers))
				
				return Response(streamDataGet(r))
			
	except:
		return 'Catalog without service'
			
	return 'Catalog without service'
	
@app.route('/external/<path:catalog>/ssa', methods=['POST', 'GET'])
@app.route('/external/<path:catalog>/SSA', methods=['POST', 'GET'])
def ExternSsa(catalog):
	int_ext = catalogIvoa.setCatalog(catalog)
	if int_ext == EXTERNAL_CATALOG:
		return ssa(catalog)
	else: 
		return 'Error'

@app.route('/<path:catalog>/tap')
@app.route('/<path:catalog>/TAP')
def InternTap(catalog):
	int_ext = catalogIvoa.setCatalog(catalog)
	if int_ext == CHIVO_CATALOG:
		return tap(catalog)
	else: 
		return 'Error'
		
def tap(catalog):
	
	catalog = urllib.quote(catalog)
	
	catalogIvoa.setCatalog(catalog)
	if 'tap' in catalogIvoa.getServices():
		return 'OK'
		
@app.route('/external/<path:catalog>/tap')
@app.route('/external/<path:catalog>/TAP')
def ExternTap(catalog):
	int_ext = catalogIvoa.setCatalog(catalog)
	if int_ext == EXTERNAL_CATALOG:
		return tap(catalog)
	else: 
		return 'Error'
		
@app.route('/<path:catalog>/TAP/<path:route>', methods = ['GET', 'POST'])
@app.route('/<path:catalog>/tap/<path:route>', methods = ['GET', 'POST'])
def InternQueryTap(catalog, route):
	int_ext = catalogIvoa.setCatalog(catalog)
	if int_ext == CHIVO_CATALOG:
		return queryTap(catalog, route)
	else: 
		return 'Error'


def queryTap(catalog,route=None):
	#catalog = urllib.quote(catalog)
	
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

				return Response(streamDataGet(r), mimetype=getResponseType(r.headers))
				
		elif request.method == "POST":
			print request.form
			print urllib.urlencode(request.form)
			print dictRoute
			r = catalogIvoa.query(urllib.urlencode(request.form), request.method, "tap",dictRoute)
			return Response(streamDataPost(r), mimetype= getResponseType(r.headers))
	return 'Bad Tap Request1'
	
@app.route('/external/<path:catalog>/TAP/<path:route>', methods = ['GET', 'POST'])
@app.route('/external/<path:catalog>/tap/<path:route>', methods = ['GET', 'POST'])
def ExternQueryTap(catalog, route):
	int_ext = catalogIvoa.setCatalog(catalog)
	if int_ext == EXTERNAL_CATALOG:
		return queryTap(catalog, route)
	else: 
		return 'Error'


@app.route('/raise')
def Praise():
	raise
	return
if __name__ == '__main__':
    app.run(debug=True)
