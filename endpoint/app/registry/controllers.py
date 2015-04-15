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
