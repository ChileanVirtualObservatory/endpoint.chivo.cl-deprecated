#import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, Response

# Import needed classes
from app.helpers.functions import *
from config import REG_URL, CHIVO_URL,TAP_REG

import requests


# Define the blueprint: 'services'
registry = Blueprint('registry', __name__)

@registry.route('/oai.xml',methods=["GET","POST"])
def reg():
	full_url = request.url.split("?")
	parameters = full_url[1] if len(full_url) == 2 else ""
	r = requests.get(REG_URL + "?" +  parameters)
	text = r.text
	text = text.replace('http://alma-be.lirae.cl:8080/cycle0fits/q/scs-cycle0-fits/scs.xml?',CHIVO_URL+'/alma/scs?')
	text = text.replace('http://alma-be.lirae.cl:8080/cycle0fits/q/siap-cycle0-fits/siap.xml?',CHIVO_URL+'/alma/sia?')
	text = text.replace("http://alma-be.lirae.cl:8080",CHIVO_URL )
	text = text.replace(TAP_REG, CHIVO_URL + "/tap")
	return Response(text, mimetype=getResponseType(r.headers))
