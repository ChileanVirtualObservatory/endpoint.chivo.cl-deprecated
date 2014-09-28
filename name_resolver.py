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
	
def toVotable(data):
	data2 = list() 
	keys= set()
	for i in data:
		data2.append(i)
		keys= keys| set(i.keys())
	keys=list(keys)
		
	#~ #Creando un nuevo votable
	votable = VOTableFile()
#~ 
	#~ # ...with one resource...
	resource = Resource()
	votable.resources.append(resource)
#~ 
	#~ 
	#~ # ... with one table
	table = Table(votable)
	resource.tables.append(table)			
	#~ 
	#~ # Define some fields
	for i in keys:
		table.fields.extend([
			Field(votable, name= i , datatype="char", arraysize="*")])
			# Field(votable, name="matrix", datatype="char", arraysize="*")])
	#Field(votable, name="matrix", datatype="double", arraysize="2x2")])
	#~ table.fields.extend([
		#~ Field(votable, name="ra", datatype="double", arraysize="*"),
		#~ Field(votable, name="dec", datatype="double", arraysize="*")
		#~ Field(votable, name="text", datatype="char", arraysize="*") ])
	#~ # Now, use those field definitions to create the numpy record arrays, with
	#~ # the given number of rows
	amount = data.count()
	
	# table.create_arrays(2)
	# rellenar = 'test1.xml', '[[1, 0], [0, 1]]'
	# Now table.array can be filled with data
	# table.array[0] = (rellenar)
	# table.array[1] = ('test2.xml', '[[0.5, 0.3], [0.2, 0.1]]')
	
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
		
		
	#table.create_arrays()
	#table.array[0] = ('test1.xml', [[1, 0], [0, 1]])
	#table.array[1] = ('test2.xml', [[0.5, 0.3], [0.2, 0.1]])
	
	votable.to_xml("new_votable.xml")
#~ 
	#~ for linea in data:
toVotable(SCS().query(0,0,100))	

        
