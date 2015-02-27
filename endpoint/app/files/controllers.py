# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, Response, \
		  stream_with_context 

from app.services.models import CustomResponse, Catalog, ChivoRegistry
from app.helpers.functions import *

import requests
#Creating objects
chivoReg = ChivoRegistry()

# Define the blueprint: 'services'
files = Blueprint('files', __name__)

@files.route('/<catalog>/file/<fitsFile>')
def getfits(catalog, fitsFile,Reg= chivoReg):
	
	cat = Reg.getCatalog(catalog)
	
	#If the catalog is not in our registry
	if cat is None:
		return render_template("404.html"), 404
		
	url = cat.filePath + fitsFile
	r = requests.get(url,stream=True)
	r.headers["Content-Disposition"] = "attachment;filename="+fitsFile
	return Response(stream_with_context(r.iter_content()) , content_type = r.headers['content-type'])
