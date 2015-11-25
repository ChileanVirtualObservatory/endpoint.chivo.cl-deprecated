
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

# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, Response, jsonify

# Import needed classes
from models import ElasticQuery
from elasticsearch.exceptions import ConnectionError, ConnectionTimeout
import sys

import urllib
import re
#Creating objects

# Define the blueprint: 'slap'
slap= Blueprint('slap', __name__)

primary_host = "http://otto.csrg.inf.utfsm.cl:9200/"
primary_index = "SL-Repository"
primary_mapping = "Spectral-Lines"
support_mapping = "support"

#Index Page
@slap.route('/slap/')
def index():
    try:
        Query = ElasticQuery(primary_host, primary_index, primary_mapping, support_mapping)
    except ConnectionError as e:
        return render_template("404.html") # TODO Replace with error template
    clean_input = {}
    input_keys = request.args.keys()
    for key in input_keys:
        clean_input[key.upper()] = request.args[key]

    if clean_input.has_key("WAVELENGHT"):
        a = clean_input["WAVELENGHT"].split("/")
        if len(a) == 2:
            min_freq = a[0]
            max_freq = a[1]
            Query.add_frequency_to_query(min_freq,max_freq)
            return jsonify(Query.send_query())
        if len(a)== 1:
            Query.add_frequency_to_query(a[0])
            return jsonify(Query.send_query())

    return render_template("index.html")