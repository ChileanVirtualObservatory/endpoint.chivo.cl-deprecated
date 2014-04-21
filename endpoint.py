import urllib

from classes import *
from func import *

from os import system
from flask import Flask, render_template, request, Response, redirect


#Application Itself
app = Flask(__name__)
chivoReg = ChivoRegistry()
extReg = VOparisRegistry() 


@app.route('/')
def index():
	return 'Index Page'

@app.route('/registry', methods = ['GET'])
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

@app.route('/external/registry', methods = ['GET'])
def extRegistry():
	return registry(extReg, True)

@app.route('/<path:catalog>')
@app.route('/<path:catalog>/')
def catalogServices(catalog, Reg = chivoReg):
	if catalog in Reg.catalogs.keys():
		i =Reg.getCatalog(catalog)
		return " ".join(i.getServices())
	return 'Catalog not found'
	
@app.route('/external/<path:catalog>')
@app.route('/external/<path:catalog>/')
def exterCatalog(catalog):
	return catalogServices(catalog, extReg)


@app.route('/<path:catalog>/sia', methods=['POST', 'GET'])
@app.route('/<path:catalog>/SIA', methods=['POST', 'GET'])
def sia(catalog, Reg = chivoReg):
	
	queryType = "sia"
	catalog = urllib.quote(catalog)

	try:
		cat = Reg.getCatalog(catalog)
		if queryType in cat.getServices():
			if request.method == "GET":
				r = cat.query(request.args, request.method, queryType) 
				if request.args:
					return Response(streamDataGet(r), mimetype= getResponseType(r.headers))
				 
				return Response(streamDataGet(r))
	except:
		return 'Catalog without service'
			
	return 'Catalog without service'
	
@app.route('/external/<path:catalog>/sia', methods=['POST', 'GET'])
@app.route('/external/<path:catalog>/SIA', methods=['POST', 'GET'])
def ExternSia(catalog):
	return sia(catalog, extReg)

@app.route('/<path:catalog>/scs', methods=['POST', 'GET'])
@app.route('/<path:catalog>/SCS', methods=['POST', 'GET'])
def scs(catalog, Reg= chivoReg):
	queryType = "scs"
	catalog = urllib.quote(catalog)
	
	try:
		cat = Reg.getCatalog(catalog)
		print cat.getServices()
		if queryType in cat.getServices():
			if request.method == "GET":
				r = cat.query(request.args, request.method, queryType ) 
				if request.args:
					return Response(streamDataGet(r), mimetype= getResponseType(r.headers))
				
				return Response(streamDataGet(r))
	except:
		return 'Catalog without service'
			
	return 'Catalog without service'

@app.route('/external/<path:catalog>/scs', methods=['POST', 'GET'])
@app.route('/external/<path:catalog>/SCS', methods=['POST', 'GET'])
def ExternScs(catalog):
	return scs(catalog, extReg)


@app.route('/<path:catalog>/ssa', methods=['POST', 'GET'])
@app.route('/<path:catalog>/SSA', methods=['POST', 'GET'])
def ssa(catalog, Reg = chivoReg):
	
	queryType = "ssa"
	catalog = urllib.quote(catalog)

	try:
		cat = Reg.getCatalog(catalog)
		if queryType in cat.getServices():
			if request.method == "GET":
				
				r = cat.query(request.args, request.method, queryType) 
				if request.args:
					return Response(streamDataGet(r), mimetype= getResponseType(r.headers))
				
				return Response(streamDataGet(r))
			
	except:
		return 'Catalog without service'
			
	return 'Catalog without service'
	
@app.route('/external/<path:catalog>/ssa', methods=['POST', 'GET'])
@app.route('/external/<path:catalog>/SSA', methods=['POST', 'GET'])
def ExternSsa(catalog):
	return ssa(catalog, extReg)

#~ @app.route('/<path:catalog>/tap')
#~ @app.route('/<path:catalog>/TAP')
#~ def InternTap(catalog):
	#~ int_ext = catalogIvoa.setCatalog(catalog)
	#~ if int_ext == CHIVO_CATALOG:
		#~ return tap(catalog)
	#~ else: 
		#~ return 'Error'
		#~ 
#~ def tap(catalog):
	#~ 
	#~ catalog = urllib.quote(catalog)
	#~ 
	#~ catalogIvoa.setCatalog(catalog)
	#~ if 'tap' in catalogIvoa.getServices():
		#~ return 'OK'
		#~ 
#~ @app.route('/external/<path:catalog>/tap')
#~ @app.route('/external/<path:catalog>/TAP')
#~ def ExternTap(catalog):
	#~ int_ext = catalogIvoa.setCatalog(catalog)
	#~ if int_ext == EXTERNAL_CATALOG:
		#~ return tap(catalog)
	#~ else: 
		#~ return 'Error'
		#~ 
#~ @app.route('/<path:catalog>/TAP/<path:route>', methods = ['GET', 'POST'])
#~ @app.route('/<path:catalog>/tap/<path:route>', methods = ['GET', 'POST'])
#~ def InternQueryTap(catalog, route):
	#~ int_ext = catalogIvoa.setCatalog(catalog)
	#~ if int_ext == CHIVO_CATALOG:
		#~ return queryTap(catalog, route)
	#~ else: 
		#~ return 'Error'
#~ 
#~ 
#~ def queryTap(catalog,route=None):
	#~ #catalog = urllib.quote(catalog)
	#~ 
	#~ catalogIvoa.setCatalog(catalog)
	#~ route = map(str,route.split("/"))
	#~ dictRoute = dict()
	#~ if len(route) > 0:
		#~ dictRoute["option"] = route[0]
	#~ if len(route) > 1:
		#~ dictRoute["qid"] = route[1]
	#~ if len(route) > 2:
		#~ dictRoute["qidOption"] = route[2]
	#~ if len(route) > 3:
		#~ dictRoute["qidOption"] = route[3]
	#~ 
	#~ if len(route) > 4:
		#~ return "Bad Tap Request"
	#~ 
	#~ if 'tap' in catalogIvoa.getServices():
		#~ 
		#~ if request.method == "GET":
				#~ r = catalogIvoa.query(None, request.method, "tap" , dictRoute)
#~ 
				#~ return Response(streamDataGet(r), mimetype=getResponseType(r.headers))
				#~ 
		#~ elif request.method == "POST":
			#~ print request.form
			#~ print urllib.urlencode(request.form)
			#~ print dictRoute
			#~ r = catalogIvoa.query(urllib.urlencode(request.form), request.method, "tap",dictRoute)
			#~ return Response(streamDataPost(r), mimetype= getResponseType(r.headers))
	#~ return 'Bad Tap Request1'
	#~ 
#~ @app.route('/external/<path:catalog>/TAP/<path:route>', methods = ['GET', 'POST'])
#~ @app.route('/external/<path:catalog>/tap/<path:route>', methods = ['GET', 'POST'])
#~ def ExternQueryTap(catalog, route):
	#~ int_ext = catalogIvoa.setCatalog(catalog)
	#~ if int_ext == EXTERNAL_CATALOG:
		#~ return queryTap(catalog, route)
	#~ else: 
		#~ return 'Error'


@app.route('/raise')
def Praise():
	raise
	return
	
	
if __name__ == '__main__':
    app.run(debug=True)
