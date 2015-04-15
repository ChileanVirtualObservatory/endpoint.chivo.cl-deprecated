"""
This file is part of ChiVO
Copyright (C) Camilo Valenzuela, Francisco Lira

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
import urllib2
import requests
import json
import threading
import copy


	
def getRegistry():
	
	#Max response items
	MAX = 1000
	#All standardid from ivoa services, those are the params from the query
	SERVICEPARAMS = {
		"tap":'ivo://ivoa.net/std/TAP',
		"sia":'ivo://ivoa.net/std/SIA',
		"ssa":'ivo://ivoa.net/std/SSA',
		"scs":'ivo://ivoa.net/std/ConeSearch',
		}

	for serv in SERVICEPARAMS.keys():		
		print "Starting "+ serv
			
		parameters ={"keywords": 'standardid:"'+SERVICEPARAMS[serv]+'"' , "max": MAX}
		r = requests.get( "http://voparis-registry.obspm.fr/vo/ivoa/1/voresources/search", params = parameters)
		entries = json.loads(r.content)['resources']
		
		catalogsList = []
		for entry in entries:
			if entry['status'] == 'active':			

				for entry_cap in entry['capabilities']:
					if entry_cap['standardid'] == SERVICEPARAMS[serv]:
						_temp = entry_cap['accessurl']
				if 'shortname' in entry.keys() and 'title' in entry.keys():
					catalogsList.append({
						'title': entry['title'],
						'shortname': entry['shortname'],
						'accessurl':_temp
						})
		jsonList = json.dumps(catalogsList)
		with open('/var/www/flask_endpoint/endpoint/app/templates/'+serv+".json", 'w') as outfile:
    			json.dump(jsonList, outfile)

def filesAlreadyCreated():
	return open("/var/www/flask_endpoint/endpoint/app/templates/tap.json") and open("/var/www/flask_endpoint/endpoint/app/templates/ssa.json") and open("/var/www/flask_endpoint/endpoint/app/templates/scs.json") and open("/var/www/flask_endpoint/endpoint/app/templates/sia.json") 		

if not filesAlreadyCreated():
	getRegistry()
