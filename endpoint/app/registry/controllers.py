#import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, Response

# Import needed classes
from app.helpers.functions import *
from config import REG_URL, CHIVO_URL

import requests

# Define the blueprint: 'services'
registry = Blueprint('registry', __name__)

@registry.route('/oai.xml',methods=["GET","POST"])
def reg():
	full_url = request.url.split("?")
	parameters = full_url[1] if len(full_url) == 2 else ""
	r = requests.get(REG_URL + "?" +  parameters)
	text = r.text.replace("http://alma-be.lirae.cl:8080",CHIVO_URL )
	return Response(text, mimetype=getResponseType(r.headers))
