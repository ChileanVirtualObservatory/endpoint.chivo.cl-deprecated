#import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, Response

# Import needed classes
from app.helpers.functions import *

import requests
#Registry URL
REG_URL = "http://alma-be.lirae.cl:8080"

# Define the blueprint: 'services'
registry = Blueprint('registry', __name__)

@registry.route('/registry/oai.xml')
def reg():
	parameters = request.args
	r = requests.get(REG_URL, params = parameters)
	return Response(r.text)
