# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, Response

from app.external.models import ExtService, ExtRegistry, VOparisRegistry
from app.services.models import ChivoRegistry
from app.helpers.functions import *

import requests
import json

#Creating objects
extReg = VOparisRegistry() 
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

@external.route('/external/registry/allTap', methods = ['GET'])
@external.route('/external/tap', methods = ['GET'])
def extRegistry1():
	internal = json.loads(registry1(chivoReg, "tap"))
	external = json.loads(registry1(extReg ,"tap"))
	return json.dumps(internal+external)
	
	
@external.route('/external/registry/allScs', methods = ['GET'])
@external.route('/external/scs', methods = ['GET'])
def extRegistry2():
	internal = json.loads(registry1(chivoReg, "scs"))
	external = json.loads(registry1(extReg ,"scs"))
	return json.dumps(internal+external)

@external.route('/external/registry/allSia', methods = ['GET'])
@external.route('/external/sia', methods = ['GET'])
def extRegistry3():
	internal = json.loads(registry1(chivoReg, "sia"))
	external = json.loads(registry1(extReg ,"sia"))
	return json.dumps(internal+external)
	
@external.route('/external/registry/allSsa', methods = ['GET'])
@external.route('/external/ssa', methods = ['GET'])
def extRegistry4():
	external = json.loads(registry1(extReg ,"ssa"))
	return json.dumps(external)
	
#External Registry
@external.route('/external/registry/', methods = ['GET'])
def extRegistry():
	internal = json.loads(registry(chivoReg))
	external = json.loads(registry(extReg))
	return json.dumps(internal+external)