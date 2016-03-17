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

import urllib2
import requests
import json
import threading
import copy


# Import flask and template operators
from flask import Flask, render_template, request, redirect

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')


## Sample HTTP error handling
#@app.errorhandler(404)
#def not_found(error):
#    return render_template('404.html'), 404

#Remove trailing slash in POST requests
#@app.before_request
#def remove_trailing_slash():
#	if request.path != '/' and request.path.endswith('/'):
#		return redirect(request.path[:-1], code=307)


# Import a module / component using its blueprint handler variable (mod_auth)
#from app.services.controllers import services as services_module
#from app.external.controllers import external as external_module
#from app.registry.controllers import registry as registry_module
from app.slap.controllers import slap as slap_module

# Register blueprint(s)
#app.register_blueprint(services_module)
#app.register_blueprint(external_module)
#app.register_blueprint(registry_module)
app.register_blueprint(slap_module)



