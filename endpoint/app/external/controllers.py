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

import app.external.models 
from app.services.models import ChivoRegistry
from app.helpers.functions import *

import requests
import json

#Creating objects
chivoReg = ChivoRegistry() 

# Define the blueprint: 'services'
external = Blueprint('external', __name__)

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
			try:
				_temp["title"] =cati.getAlias()["title"] if cati.getAlias() else cati.title
				_temp["shortname"] = cati.getAlias()["shortname"] if cati.getAlias() else cati.shortname
				unfiltered = cati.getAlias()["capabilities"] if cati.getAlias() else cati.capabilities
			except:
				_temp["title"] = cati.title
				_temp["shortname"] = cati.shortname
				unfiltered = cati.capabilities
			for s in unfiltered:
				if s["standardid"] == SERVICEPARAMS[service]:
					_temp["accessurl"] = s["accessurl"]
			cat.append(_temp)
	return json.dumps(cat)

def loadJson(service):
	file = open("/var/www/flask_endpoint/endpoint/app/templates/"+service+".json")
	json_data = json.load(file)
	return json_data

@external.route('/external/registry/allTap', methods = ['GET'])
@external.route('/external/tap', methods = ['GET'])
def extRegistry1():
	internal = json.loads(registry1(chivoReg, "tap"))
	external = json.loads(loadJson('tap'))
	return json.dumps(internal+external)

	
@external.route('/external/registry/allScs', methods = ['GET'])
@external.route('/external/scs', methods = ['GET'])
def extRegistry2():
	internal = json.loads(registry1(chivoReg, "scs"))
	external = json.loads(loadJson('scs'))
	return json.dumps(internal+external)

@external.route('/external/registry/allSia', methods = ['GET'])
@external.route('/external/sia', methods = ['GET'])
def extRegistry3():
	internal = json.loads(registry1(chivoReg, "sia"))
        external = json.loads(loadJson('sia'))	
	return json.dumps(internal+external)
	
@external.route('/external/registry/allSsa', methods = ['GET'])
@external.route('/external/ssa', methods = ['GET'])
def extRegistry4():
        external = json.loads(loadJson('ssa'))	
	return json.dumps(external)
	
