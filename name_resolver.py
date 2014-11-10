import json
from pymongo import MongoClient
from astropy import units as u
from astropy.io.votable.tree import VOTableFile, Resource, Table, Field
from bson import BSON
from bson import json_util

class ChivoBib:
	def __init__(self):
		#Making the connection with mongo
		client = MongoClient('localhost', 27017)
		db = client.chivo
		self.collection = db.name_resolver			
	def scs(self,ra, dec, sr):
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
		return toVotable(data)
	
	def nameResolver(self,name):
		query = {'MAIN_ID': {'$regex': name}}
		data = self.collection.find(query)
		return json_util.dumps(data, sort_keys=True, indent=4, default=json_util.default)
		
		
	
def toVotable(data):
	data2 = list() 
	keys= set()
	for i in data:
		data2.append(i)
		keys= keys| set(i.keys())
	keys=list(keys)
		
	#Creating un nuevo votable
	votable = VOTableFile()

	# ...with one resource...
	resource = Resource()
	votable.resources.append(resource)

	
	# ... with one table
	table = Table(votable)
	resource.tables.append(table)			
	
	# Define some fields
	for i in keys:
		table.fields.extend([
			Field(votable, name= i , datatype="char", arraysize="*")])
	amount = data.count()
	
	table.create_arrays(amount)
	lap = 0
	for i in data2:
		num = 0
		for j in keys:
			if num == 0:
				num = num + 1
				if j in i.keys():
					rellenar = str(i[j]),
				else:
					rellenar = "' '",
			else:
				if j in i.keys():
					rellenar += str(i[j]),
				else:
					rellenar +=  "' '",
		table.array[lap] = (rellenar)
		lap = lap + 1	
	
	table = votable.to_xml("temp.xml")
	f = open("temp.xml")
	return f.read()
		
	
	

        
