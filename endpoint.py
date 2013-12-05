import subprocess
import urllib
import urllib2
import redis 
import requests
from os import system
from flask import Flask, render_template, request, Response, redirect
app = Flask(__name__)

SERVER_TAP1	= 'http://localhost:8080/cadcSampleTAP/sync'
SERVER_TAP	= 'http://wfaudata.roe.ac.uk/twomass-dsa/TAP'
SERVER_SCS	= 'http://wfaudata.roe.ac.uk/twomass-dsa/DirectCone?DSACAT=TWOMASS&DSATAB=twomass_psc'
SERVER_SSA	= 'http://wfaudata.roe.ac.uk/6dF-ssap/?'
SERVER_SIA	= 'http://irsa.ipac.caltech.edu/ibe/sia/wise/prelim/p3am_cdd?'


redisConn = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    return 'Index page'

@app.route('/alma/<query>', methods=['POST', 'GET'])
@app.route('/alma/<query>/<option>', methods=['POST', 'GET'])
@app.route('/alma/<query>/<option>/<qid>', methods=['POST', 'GET'])
@app.route('/alma/<query>/<option>/<qid>/<qidOption>', methods=['POST', 'GET'])
@app.route('/alma/<query>/<option>/<qid>/<qidOption>/<qidOptionRequest>', methods=['POST', 'GET'])
def chivo_query(query,qid=None,option=None, qidOption = None, qidOptionRequest = None):
	CHUNK = 1024
	if query.lower() == 'tap':
		if option.lower() == "capabilities":
			return redirect(SERVER_TAP +"/" + option)
		
		
		if option.lower() == "sync":
			if request.method == 'POST':
				
				data = urllib.urlencode(request.form)
				req = urllib2.Request(SERVER_TAP+"/"+option, data)
				response = urllib2.urlopen(req)
				
				def generate():
					for the_page in iter(lambda: response.read(CHUNK), ''):
						yield the_page
	
				return Response(generate(), mimetype='text/xml')
			
			elif request.method == 'GET':
				
				#r = requests.get(SERVER_SCS, params=request.args,stream=True)
				return 'Bad Tad Request'
				
		elif option.lower() == "async":
			if request.method == 'POST':
				if qid == None:				
					data = urllib.urlencode(request.form)
					req = urllib2.Request(SERVER_TAP+"/"+option, data)
					response = urllib2.urlopen(req)
					def generate():
						for the_page in iter(lambda: response.read(CHUNK), ''):
							yield the_page
		
					return Response(generate(), mimetype='text/xml')
				else:
					return qid
			
			elif request.method == 'GET':
				params  = "/" + option
				if qid:
					params += "/" + qid
				if qidOption:
					params += "/" + qidOption	
				if qidOptionRequest:
					params += "/" + qidOptionRequest
				r = requests.get(SERVER_TAP + params,stream=True)
				return r.content
					
		return 'Bad Tap Request'

	if query == 'scs':
		if request.method == 'GET':
			#SCS Request GET 
			#values = {}
			#VERB	= 0

			#values['RA']	= request.args.get('RA')
			#values['DEC']	= request.args.get('DEC')
			#values['SR']	= request.args.get('SR')
			#VERB			= request.args.get('VERB')

			#Validation of request

			#if VERB is not None:
			#	values['VERB'] = VERB

			#Run SCS request
			
			
			#Testing Redis in SCS
			

			parameters=request.args
			key = "scs;"+str(parameters)
			r = redisConn.get(key)
			if(r):
				return r
			else:
				r = requests.get(SERVER_SCS, params= parameters,stream=True)
				redisConn.set(key, r.content)
				redisConn.expire(key,1 * 24 * 60 * 60)
				return r.content
		
		return 'Bad SCS Request'

	if query == 'sia':
		if request.method == 'GET':
			#SIA Request GET 
			#POS = request.args.get('POS')
			#SIZE = request.args.get('SIZE')
			#FORMAT = request.args.get('FORMAT')
			#NAXIS = request.args.get('NAXIS')
			#PROJ = request.args.get('PROJ')
			#CFRAME = request.args.get('CFRAME')
			#EQUINOX = request.args.get('EQUINOX')
			
			#Validation of request

			#Run SIA request
			
			r = requests.get(SERVER_SIA, params= request.args,stream=True)
			
			
			def generate():
				for line in r.iter_lines():
    					if line: # filter out keep-alive new lines
        					yield line
			
			return Response(generate(), mimetype='text/xml')

			

		return 'Bad SIA Request'

	if query == 'ssa':
		if request.method == 'GET':
			#SSA Request GET
			#POS = request.args.get('POS')
			#SIZE = request.args.get('SIZE')

			#Validation of request

			#Run SSA request
			r = requests.get(SERVER_SSA, params=request.args,stream=True)
	
			return r.content
		
		return 'Bad SSA Request'
	return 'Bad Request'


@app.errorhandler(404)
def page_not_found(error):
	return 'This page does not exist', 404

if __name__ == '__main__':
    app.run(debug=True)
