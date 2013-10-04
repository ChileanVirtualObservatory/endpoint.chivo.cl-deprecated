import subprocess
import urllib
import urllib2
import requests
from os import system
from flask import Flask, render_template, request
app = Flask(__name__)

SERVER_TAP = 'http://localhost:8080/cadcSampleTAP/sync'
SERVER_SCS = 'http://wfaudata.roe.ac.uk/twomass-dsa/DirectCone?DSACAT=TWOMASS&DSATAB=twomass_psc'
SERVER_SSA = 'http://wfaudata.roe.ac.uk/6dF-ssap/?'
SERVER_SIA = 'http://skyview.gsfc.nasa.gov/cgi-bin/vo/sia.pl?survey=2mass&'

@app.route('/')
def index():
    return 'Index page'

@app.route('/chivo/<query>', methods=['POST', 'GET'])
def chivo_query(query):
	if query == 'tap':
		if request.method == 'POST':
			#Consulta TAP POST
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

			#Validar Consulta
	
			#Ejecutar consulta TAP 	
			data = urllib.urlencode(request.form)
			req = urllib2.Request(SERVER_TAP, data)
			response = urllib2.urlopen(req)
			the_page = response.read()
	
			return the_page

		if request.method == 'GET':
			#Consulta TAP GET

			#Validar Consulta
	
			#Ejecutar consulta TAP 	
			r = requests.get(SERVER_SCS, params=request.args)
			return r.content

		return 'Bad TAP Request'

	if query == 'scs':
		if request.method == 'GET':
			#Consulta SCS GET 
			#values = {}
			#VERB	= 0

			#values['RA']	= request.args.get('RA')
			#values['DEC']	= request.args.get('DEC')
			#values['SR']	= request.args.get('SR')
			#VERB			= request.args.get('VERB')

			#Validar Consulta

			#if VERB is not None:
			#	values['VERB'] = VERB

			#Ejecutar consulta SCS 
			r = requests.get(SERVER_SCS, params=request.args)
	
			return r.content
		
		return 'Bad SCS Request'

	if query == 'sia':
		if request.method == 'GET':
			#Consulta SIA GET 
			#POS = request.args.get('POS')
			#SIZE = request.args.get('SIZE')
			#FORMAT = request.args.get('FORMAT')
			#NAXIS = request.args.get('NAXIS')
			#PROJ = request.args.get('PROJ')
			#CFRAME = request.args.get('CFRAME')
			#EQUINOX = request.args.get('EQUINOX')
			
			#values = {'POS' : POS, 'SIZE' : SIZE , 'FORMAT' : FORMAT , 'NAXIS' : NAXIS , 'PROJ' : PROJ , 'CFRAME' : CFRAME , 'EQUINOX' : EQUINOX}

			#Validar argumentos 

			#Ejecutar consulta al servidor SIA
			r = requests.get(SERVER_SIA, params=request.args)
			return r.content

		return 'Bad SIA Request'

	if query == 'ssa':
		if request.method == 'GET':
			#Consulta SSA GET
			#POS = request.args.get('POS')
			#SIZE = request.args.get('SIZE')

			#Validar argumentos

			#Ejecutar consulta SSA
			r = requests.get(SERVER_SSA, params=request.args)
	
			return r.content
		
		return 'Bad SSA Request'

if __name__ == '__main__':
    app.run(debug=True)
