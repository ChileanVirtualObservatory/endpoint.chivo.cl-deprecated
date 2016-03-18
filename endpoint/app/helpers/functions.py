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

from app.services.models import Catalog, Registry 

#Functions for data streaming

#Iters lines from GET response object
def streamDataGet(r):
	for line in r.iter_lines():
			if line: # filter out keep-alive new lines
				yield line
	

#Iters lines from POST response object
def streamDataPost(r):
	CHUNK = 1024
	for the_page in iter(lambda: r.read(CHUNK), ''):
		yield the_page

#Read the xml response type
def getResponseType(content):
	if "content-type" in content.keys():
		return content["content-type"].split(";")[0]
	else:
		return 'text/xml'

