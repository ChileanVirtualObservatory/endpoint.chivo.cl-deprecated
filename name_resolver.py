from pymongo import MongoClient
from astropy import units as u
from astropy.io.votable.tree import VOTableFile, Resource, Table, Field
class SCS:
	def __init__(self):
		#Making the connection with mongo
		client = MongoClient('localhost', 27017)
		db = client.chivo
		self.collection = db.name_resolver			
	def query(self,ra, dec, sr):
		#Transforming sr from degree to radians
		sr = sr * u.degree
		sr = sr.to(u.rad)
		
		#Generating the circular query
		params = {'loc':
				{'$geoWithin':
					{'$centerSphere':
						[[ra,dec], sr.value]}}}
		#Sending the request
		data = self.collection.find(params)
		return data		
	
	def _toVotable(meta,data):
		#Creando un nuevo votable
		votable = VOTableFile()

		# ...with one resource...
		resource = Resource()
		votable.resources.append(resource)

		
		# ... with one table
		table = Table(votable)
		resource.tables.append(table)			
		
		# Define some fields
		table.fields.extend([
			Field(votable, name="ra", datatype="double", arraysize="*"),
Field(votable, name="dec", datatype="double", arraysize="*")
        		Field(votable, name="text", datatype="char", arraysize="*") ])
		# Now, use those field definitions to create the numpy record arrays, with
		# the given number of rows
		amount = data.count()
		table.create_arrays(amount)

		for linea in data:
			

        
