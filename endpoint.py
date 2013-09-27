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

@app.route('/')
def index():
    return 'Index page'

#GET -> request.args.get('key', '')
#POST -> request.form['key']

@app.route('/chivo/<query>', methods=['POST', 'GET'])
def chivo_query(query):
	if query == 'tap':
		if request.method == 'POST':
			#Consulta hecha al servidor TAP
			query = request.form
	 
			#Validar Consulta 
			#TODO: checkear parametros posibles de TAP y validarlos
	
			#Ejecutar consulta al servidor TAP 
			#TODO: crear un arreglo de servidores posibles RESOURCES y hacer el request para cada RESOURCE requerido en al consulta 
			url = SERVER_TAP
			values = {'REQUEST' : query['REQUEST'],
			          'LANG' : query['LANG'],
			          'QUERY' : query['QUERY']}
	
			data = urllib.urlencode(values)
			req = urllib2.Request(url, data)
			response = urllib2.urlopen(req)
			the_page = response.read()
	
			return the_page

	if query == 'scs':
		if request.method == 'GET':
			#Argumentos consulta metodo GET 
			#TODO: nombre parametros
			RA = request.args.get('ra')
			DEC = request.args.get('dec')
			RADIUS = request.args.get('RADIUS')
	        
			print RA
			print DEC
			print RADIUS

			#ejemplo
			#get = http://wfaudata.roe.ac.uk/twomass-dsa/DirectCone\?DSACAT\=TWOMASS\&DSATAB\=twomass_psc\&ra\=21\&dec\=15\&RADIUS\=1
			values = {'ra' : RA, 'dec' : DEC, 'RADIUS' : RADIUS}

			r = requests.get(SERVER_SCS, params=values)
 
			#Validar argumentos 
			#TODO: revisar nombres de los parametros y si son case sensitive
	
			#Ejecutar consulta al servidor SCS 
			#TODO: buscar un servicio que soporte SCS para probar mientras y ejecutar el request
	
			#Retornar respuesta servidor TAP %TODO
			
			return r.content
			#return 'SCSP Under construction'
		
		return 'Bad Request'

	if query == 'sia':
		if request.method == 'GET':
			#Argumentos consulta metodo GET 
			#TODO: revisar parametros de busqueda y si es que solo soporta GET
	
			#Validar argumentos 
			#TODO: revisar nombres de los parametros y si son case sensitive
	
			#Ejecutar consulta al servidor SIA
			#TODO: buscar un servicio que soporte SIA para probar mientras y ejecutar el request
	
			#Retornar respuesta servidor TAP %TODO
			return 'SIAP Under construction'
		
		return 'Bad Request'


	if query == 'ssa':
		if request.method == 'GET':
			values = {'POS' : '22.438,-17.2',
			          'SIZE' : '0.02'}

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
