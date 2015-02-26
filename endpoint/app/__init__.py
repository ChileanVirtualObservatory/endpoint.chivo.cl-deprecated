import urllib2
import requests
import json
import threading
import copy


# Import flask and template operators
from flask import Flask, render_template, request

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')


## Sample HTTP error handling
#@app.errorhandler(404)
#def not_found(error):
#    return render_template('404.html'), 404

#Remove trailing slash in POST requests
@app.before_request
def remove_trailing_slash():
	if request.path != '/' and request.path.endswith('/') and request.method == "POST":
		return redirect(request.path[:-1], code=307)


# Import a module / component using its blueprint handler variable (mod_auth)
from app.services.controllers import services as services_module
from app.files.controllers import files as files_module
#from app.external.controllers import external as external_module

# Register blueprint(s)
app.register_blueprint(services_module)
app.register_blueprint(files_module)
#app.register_blueprint(external_module)




