#import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, Response

# Import needed classes
from app.helpers.functions import *

import requests
#Registry URL
REG_URL = "http://alma-be.lirae.cl:8080/oai.xml"

# Define the blueprint: 'services'
registry = Blueprint('registry', __name__)

@registry.route('/oai.xml',methods=["GET","POST"])
def reg():
	parameters = request.url.split("?")[1]
	r = requests.get(REG_URL + "?" +  parameters)
	return Response(r.text, mimetype=getResponseType(r.headers))
