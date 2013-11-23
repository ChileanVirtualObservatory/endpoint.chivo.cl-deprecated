from __future__ import absolute_import

import subprocess
import urllib
import urllib2
import redis 
import requests
from os import system
from flask import Flask, render_template, request
app = Flask(__name__)

SERVER_TAP1	= 'http://localhost:8080/cadcSampleTAP/sync'
SERVER_TAP	= 'http://wfaudata.roe.ac.uk/twomass-dsa/TAP/sync'
SERVER_SCS	= 'http://wfaudata.roe.ac.uk/twomass-dsa/DirectCone?DSACAT=TWOMASS&DSATAB=twomass_psc'
SERVER_SSA	= 'http://wfaudata.roe.ac.uk/6dF-ssap/?'
SERVER_SIA	= 'http://skyview.gsfc.nasa.gov/cgi-bin/vo/sia.pl?survey=2mass&'

redisConn = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    return 'Index page'

@app.route('/chivo/<query>', methods=['POST', 'GET'])
def chivo_query(query):
	if query == 'tap':
		if request.method == 'POST':
			#TAP Request POST
			#query = request.form

			#REQUEST	= query['REQUEST']
			#LANG		= query['LANG']
			#QUERY		= query['QUERY']
			#POS		= query['POS']
			#FROM		= query['FROM']
			#SIZE		= query['SIZE']

			#MAXREC		= query['MAXREC']
			#RUNID		= query['RUNID']
			#UPLOAD		= query['UPLOAD']

			#Validation of request
	
			#Run TAP request
			
			data = urllib.urlencode(request.form)
			req = urllib2.Request(SERVER_TAP, data)
			response = urllib2.urlopen(req)
			the_page = response.read()
	
			return the_page

		if request.method == 'GET':
			#TAP Request GET

			#Validation of request
	
			#Run TAP request  	
			r = requests.get(SERVER_SCS, params=request.args)
			return r.content

		return 'Bad TAP Request'

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
			#else:
			#	r = requests.get(SERVER_SCS, params= parameters)
			#	redisConn.set(key, r.content)
			#	#redisConn.expire(key,120)
			#	return r.content
		
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
			
			
			r = requests.get(SERVER_SIA, params)

			return r.content

		return 'Bad SIA Request'

	if query == 'ssa':
		if request.method == 'GET':
			#SSA Request GET
			#POS = request.args.get('POS')
			#SIZE = request.args.get('SIZE')

			#Validation of request

			#Run SSA request
			r = requests.get(SERVER_SSA, params=request.args)
	
			return r.content
		
		return 'Bad SSA Request'
	return 'Bad Request'


@app.errorhandler(404)
def page_not_found(error):
	return 'This page does not exist', 404

if __name__ == '__main__':
    app.run(debug=True)
