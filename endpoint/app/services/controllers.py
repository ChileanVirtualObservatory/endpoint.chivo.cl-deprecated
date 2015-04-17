#This file is part of ChiVO, the Chilean Virtual Observatory
#A project sponsored by FONDEF (D11I1060)
#Copyright (C) 2015 Universidad Tecnica Federico Santa Maria Mauricio Solar
#                                                            Marcelo Mendoza
#                   Universidad de Chile                     Diego Mardones
#                   Pontificia Universidad Catolica          Karim Pichara
#                   Universidad de Concepcion                Ricardo Contreras
#                   Universidad de Santiago                  Victor Parada
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, Response

# Import needed classes
from app.services.models import CustomResponse, Catalog, ChivoRegistry
from app.helpers.functions import *
from config import CHIVO_URL

import urllib
import re
#Creating objects
chivoReg = ChivoRegistry()

# Define the blueprint: 'services'
services = Blueprint('services', __name__)

#Index Page
@services.route('/')
def index():
	return render_template("index.html")


#Tap Sync Query, only POST method
@services.route('/<catalog>/tap/sync', methods = ['POST'])
def syncTap(catalog, Reg = chivoReg):
	data = urllib.urlencode(request.form)
	cat = Reg.getCatalog(catalog)
	#If the catalog is not in our registry
	if cat is None:
		return render_template("404.html"), 404
	#If the catalog has 'tap' service, we make the request
	if 'tap' in cat.getServices():
		
		res = cat.tapSyncQuery(data)
		if type(res) is str:
			return res
		return Response(res.text , mimetype=getResponseType(res.headers))
	return 'Error2', 404

#Show tap tables from a catalog
@services.route('/<catalog>/tap/tables')
def tapTables(catalog, Reg= chivoReg):
	cat = Reg.getCatalog(catalog)
	#Validate catalog
	if cat is None:
		return render_template("404.html"), 404
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapTables()
		return Response(streamDataGet(r), mimetype=getResponseType(r.headers))

#Show tap capabilities from a catalog
@services.route('/<catalog>/tap/capabilities/')
def tapCapability(catalog, Reg= chivoReg):
	cat = Reg.getCatalog(catalog)
	#Validate catalog
	if cat is None:
		return render_template("404.html"), 404
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapCapabilities()
		return Response(streamDataGet(r), mimetype=getResponseType(r.headers))

#Show tap availability from a catalog		
@services.route('/<catalog>/tap/availability/')
def tapAvailability(catalog, Reg= chivoReg):
	cat = Reg.getCatalog(catalog)
	#Validate catalog
	if cat is None:
		return render_template("404.html"), 404
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapAvailability()
		return Response(streamDataGet(r), mimetype=getResponseType(r.headers))
		
#Tap Async Query, Post method for making request, and Get for getting all requests made
@services.route('/<catalog>/tap/async', methods=['POST', 'GET'])
def tapAsync(catalog, Reg= chivoReg):
	data = urllib.urlencode(request.form)
	cat = Reg.getCatalog(catalog)

	print data
	#If the catalog is not in our registry
	if cat is None:
		return render_template("404.html"), 404
	#If the catalog has 'tap' service, we make the request
	if 'tap' in cat.getServices():
		r = cat.tapAsyncQuery(data,request.method)
		if request.method == "POST":
			res = r.read()
			jobid = re.findall('<uws:jobId>(.*)</uws:jobId>', res)[0]
			return redirect(CHIVO_URL+"/"+cat.shortname+'/tap/async/'+jobid, code = 303)
		else:
			return Response(streamDataGet(r), mimetype=getResponseType(r.headers))		
		
#Tap Async Job Info
@services.route('/<catalog>/tap/async/<jobId>/', methods=['GET'])
@services.route('/<catalog>/TAP/async/<jobId>/', methods=['GET'])
def tapAsyncJob(catalog, jobId , Reg = chivoReg):
	cat = Reg.getCatalog(catalog)
	#Validate catalog
	if cat is None:
		return render_template("404.html"), 404
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapAsyncJob(jobId)
		return Response(streamDataGet(r), mimetype=getResponseType(r.headers))


@services.route('/<catalog>/tap/async/<jobId>/results/', methods=['GET'])
@services.route('/<catalog>/TAP/async/<jobId>/results/', methods=['GET'])
def tapAsyncResults(catalog, jobId , Reg = chivoReg):
	cat = Reg.getCatalog(catalog)
	#Validate catalog
	if cat is None:
		return render_template("404.html"), 404
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapAsyncResults(jobId)
		return Response(streamDataGet(r), mimetype=getResponseType(r.headers))

@services.route('/<catalog>/tap/async/<jobId>/results/<path:result>', methods=['GET'])
@services.route('/<catalog>/TAP/async/<jobId>/results/<path:result>', methods=['GET'])
def tapAsyncResult(catalog, jobId, result, Reg = chivoReg):
	cat = Reg.getCatalog(catalog)
	#Validate catalog
	if cat is None:
		return render_template("404.html"), 404
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapAsyncResult(jobId,result)
		return Response(streamDataGet(r), mimetype=getResponseType(r.headers))

@services.route('/<catalog>/tap/async/<jobId>/quote/', methods=['GET'])
@services.route('/<catalog>/TAP/async/<jobId>/quote/', methods=['GET'])
def tapAsyncQuote(catalog, jobId , Reg = chivoReg):
	cat = Reg.getCatalog(catalog)
	#Validate catalog
	if cat is None:
		return render_template("404.html"), 404
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapAsyncQuote(jobId)
		return Response(streamDataGet(r), mimetype=getResponseType(r.headers))
		
@services.route('/<catalog>/tap/async/<jobId>/destruction/', methods=['GET'])
@services.route('/<catalog>/TAP/async/<jobId>/destruction/', methods=['GET'])
def tapAsyncDestruction(catalog, jobId , Reg = chivoReg):
	cat = Reg.getCatalog(catalog)
	#Validate catalog
	if cat is None:
		return render_template("404.html"), 404
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapAsyncDestruction(jobId)
		return Response(streamDataGet(r), mimetype=getResponseType(r.headers))		
		
@services.route('/<catalog>/tap/async/<jobId>/executionduration/', methods=['GET'])
@services.route('/<catalog>/TAP/async/<jobId>/executionduration/', methods=['GET'])
def tapAsyncDuration(catalog, jobId , Reg = chivoReg):
	cat = Reg.getCatalog(catalog)
	#Validate catalog
	if cat is None:
		return render_template("404.html"), 404
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapAsyncDuration(jobId)
		return Response(streamDataGet(r), mimetype=getResponseType(r.headers))

@services.route('/<catalog>/tap/async/<jobId>/phase', methods= ['GET', 'POST'])
@services.route('/<catalog>/TAP/async/<jobId>/phase', methods= ['GET', 'POST'])
def tapAsyncPhase(catalog, jobId, Reg = chivoReg):

	cat = Reg.getCatalog(catalog)
	data = urllib.urlencode(request.form)
	#Validate catalog
	if cat is None:
		return render_template("404.html"), 404
	#Validate service
	if 'tap' in cat.getServices():
		r = cat.tapPhase(jobId, request.method, data)
		if request.method == "GET":
			return Response(streamDataGet(r), mimetype=getResponseType(r.headers))
		elif request.method == 'POST':
			return redirect(url_for('.tapAsyncJob',catalog=catalog, jobId=jobId), code = 303)


#SIA,SSA,SCS Query method
@services.route('/<catalog>/<service>')
def query(catalog,service, Reg = chivoReg, methods=['GET']):

	#Looking for catalog.
	cat = Reg.getCatalog(catalog)

	if cat is None:
		return render_template("404.html"), 404

	#Send request if the catalog has the service.
	if service.lower() in cat.getServices():
		#Making the request
		r = cat.query(request.args, request.method, service.lower()) 
		return Response(r.text, mimetype= getResponseType(r.headers))
	
	return render_template("404.html"), 404
