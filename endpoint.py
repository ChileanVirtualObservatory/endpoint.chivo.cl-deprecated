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
			#Consulta hecha al servidor TAP
			query = request.formi
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
		return 'Bad Request'

	if query == 'scs':
		if request.method == 'GET':
			#Argumentos consulta metodo GET 
			#TODO: nombre parametros
			RA = request.args.get('ra')
			DEC = request.args.get('dec')
			RADIUS = request.args.get('RADIUS')

			values = {'ra' : RA, 'dec' : DEC, 'RADIUS' : RADIUS}

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
			
			values = {'POS' : POS, 'SIZE' : SIZE}
			
			r = requests.get(SERVER_SIA, params=values)

			#Argumentos consulta metodo GET 
			#TODO: revisar parametros de busqueda y si es que solo soporta GET
	
			#Validar argumentos 
			#TODO: revisar nombres de los parametros y si son case sensitive
	
			#Ejecutar consulta al servidor SIA
			#TODO: buscar un servicio que soporte SIA para probar mientras y ejecutar el request
	
			#Retornar respuesta servidor TAP %TODO
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
