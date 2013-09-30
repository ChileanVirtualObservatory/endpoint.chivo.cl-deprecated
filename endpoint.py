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
			query = request.form

			REQUEST		= query['REQUEST']
			LANG		= query['LANG']
			QUERY		= query['QUERY']
			POS			= query['POS']
			FROM		= query['FROM']
			SIZE		= query['SIZE']

			MAXREC		= query['MAXREC']
			RUNID		= query['RUNID']
			UPLOAD		= query['UPLOAD']

			values = {'REQUEST' : query['REQUEST'],
			          'LANG' : query['LANG'],
			          'QUERY' : query['QUERY']}
	 
			#Validar Consulta 
			#TODO: checkear parametros posibles de TAP y validarlos
	
			#Ejecutar consulta al servidor TAP 
			#TODO: crear un arreglo de servidores posibles RESOURCES y hacer el request para cada RESOURCE requerido en al consulta 
	
			data = urllib.urlencode(values)
			req = urllib2.Request(SERVER_TAP, data)
			response = urllib2.urlopen(req)
			the_page = response.read()
	
			return the_page

		if request.method == 'GET':
			#Consulta TAP GET

			#Parametros Query	
			RA      = request.args.get('ra')

		
		return 'Bad Request'

	if query == 'scs':
		if request.method == 'GET':
			#Argumentos consulta metodo GET 
			#TODO: nombre parametros
			RA		= request.args.get('ra')
			DEC		= request.args.get('dec')
			SR		= request.args.get('SR')
			VERB	= request.args.get('VERB')

			values = {'ra' : RA, 'dec' : DEC, 'SR' : SR}

			r = requests.get(SERVER_SCS, params=values)
 
			#Validar argumentos 
			#TODO: revisar nombres de los parametros y si son case sensitive
	
			#Ejecutar consulta al servidor SCS 
			#TODO: buscar un servicio que soporte SCS para probar mientras y ejecutar el request
	
			#Retornar respuesta servidor TAP %TODO
			return r.content
		
		return 'Bad Request'

	if query == 'sia':
		if request.method == 'GET':
			POS = request.args.get('POS')
			SIZE = request.args.get('SIZE')
			FORMAT = request.args.get('FORMAT')
			NAXIS = request.args.get('NAXIS')
			PROJ = request.args.get('PROJ')
			CFRAME = request.args.get('CFRAME')
			EQUINOX = request.args.get('EQUINOX')
			
			values = {'POS' : POS, 'SIZE' : SIZE , 'FORMAT' : FORMAT , 'NAXIS' : NAXIS , 'PROJ' : PROJ , 'CFRAME' : CFRAME , 'EQUINOX' : EQUINOX}
			r = requests.get(SERVER_SIA, params=values)

			#Argumentos consulta metodo GET 
			#TODO: revisar parametros de busqueda y si es que solo soporta GET
	
			#Validar argumentos 
			#TODO: revisar nombres de los parametros y si son case sensitive
	
			#Ejecutar consulta al servidor SIA
			#TODO: buscar un servicio que soporte SIA para probar mientras y ejecutar el request
	
			#Retornar respuesta servidor TAP %TODO
			arch = open("prueba.txt", "w")
			arch.write(r.text)
			arch.close()
			return r.content

		
		return 'Bad Request'

	if query == 'ssa':
		if request.method == 'GET':
			POS = request.args.get('POS')
			SIZE = request.args.get('SIZE')

			values = {'POS' : POS, 'SIZE' : SIZE}

			r = requests.get(SERVER_SSA, params=values)

			#Argumentos consulta metodo GET 
			#TODO: revisar parametros de busqueda y si es que solo soporta GET
	
			#Validar argumentos 
			#TODO: revisar nombres de los parametros y si son case sensitive
	
			#Ejecutar consulta al servidor SSA
			#TODO: buscar un servicio que soporte SSA para probar mientras y ejecutar el request
	
			#Retornar respuesta servidor TAP %TODO
			return r.content
		
		return 'Bad Request'

if __name__ == '__main__':
    app.run(debug=True)
