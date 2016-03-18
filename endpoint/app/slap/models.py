import elasticsearch
from multiprocessing import cpu_count
from multiprocess import Pool  # Allows for efficient parallel Map, To install use pip install multiprocess
import pprint #TODO REMOVE THIS IMPORT!
import json


primary_host = "http://otto.csrg.inf.utfsm.cl:9200/"
primary_index = "SL-Repository"
primary_mapping = "Spectral-Lines"
support_mapping = "support"

def isFloat(value):
  try:
    float(value)
    return True
  except:
    return False

def toFloat(value):
	if isFloat(value):
		 return float(value)
	else:
		raise ValueError("Value is not Number")


class ElasticQuery():
	"""
	Class designed to retrieve easily SLAP data from Elasticsearch
	"""

	def __init__(self, host, primary_index, primary_mapping, SLAP):
		self.__host = host
		self.__primary_index = primary_index.lower()
		self.__primary_mapping = primary_mapping
		self.__connection = elasticsearch.Elasticsearch(hosts=self.__host)
		number = self.__connection.count(index=self.__primary_index)["count"]
		self.__max_result_size = number #if number < 10000 else 10000

		self.__numeric_fields = SLAP["NUMERIC_FIELDS"]
		self.__slap_fields = SLAP["PARAMETERS"]
		self.__queryable_fields = SLAP["QUERYABLE_FIELDS"]
		self.__scroll_time = "1m"

		self.__output_api="1.0"
		self.__error_list= []
		self.__supported_slap_versions = [1.0, 2.0]

	def __extractor(self, element):
		keys = element["fields"].keys()
		keys.sort()

		output = []
		for key in keys:
			output.append(element["fields"][key][0])
		return output

	def __metadata_extractor(self, sample):
		med = sample[0]["fields"].keys()
		med.sort()
		out = []
		for key in med:
			out.append(self.__slap_fields[key.upper()])
		return out

	def send_query(self, query, timeout=180):
		self.__parser(query)
		if self.query == -1:
			raise ValueError("You must enter at least one search parameter")
		else:
			data = self.__connection.search(index=self.__primary_index, doc_type=self.__primary_mapping,
											body=json.dumps(self.query), size=self.__max_result_size,
											request_timeout=timeout, scroll=self.__scroll_time, fields=self.__queryable_fields)

			query_size = data["hits"]["total"]
			query_time = data["took"]
			query_data = data["hits"]["hits"]

			metadata = self.__metadata_extractor(query_data) if len(query_data) > 0 else []

			pool = Pool(cpu_count())
			filtered_data = pool.map(self.__extractor, query_data)
			pool.close()
			pool.join()
			data.clear()
			del query_data[:]


			if self.__output_api == 1.0:
				return self.convert_to_XML(filtered_data,metadata,query_size,query_time)
			elif self.__output_api == 2.0:
				return self.convert_to_JSON(filtered_data,metadata,query_size,query_time)
			else:
				return self.convert_to_XML(filtered_data,metadata,query_size,query_time)

	def convert_to_XML(self,data, metadata, size, time):
		return self.convert_to_JSON(data,metadata,size,time)

	def convert_to_JSON(self,data, metadata, size, time):
		return json.dumps({"results": data, "time": time, "total": size, "metadata": metadata})

	def __range(self, limits, param):
		q = {}
		if limits[0] and limits[1]:
			q = {"gte": float(limits[0]), "lte": float(limits[1])}
		elif limits[1]:
			q = {"lte": float(limits[1])}
		elif limits[0]:
			q = {"gte": float(limits[0])}
		else:
			raise ValueError("You must specify either a maximum or minimum")

		return {"range": {param: q}}

	def __equality(self, value, param):
		processed_value = value
		query_type = "match"
		if param.upper() in self.__numeric_fields:
			processed_value = float(value)
			query_type = "term"
		# This will match EXACTLY the number.
		# I.E. if value is 16.3, will only match 16.30, 16.3000, 16.3000000 and so on, but not 16.30000001

		return {query_type: {param: processed_value}}

	def __constrain_parser(self, value, param):
		splited_constrains = value.split(",")
		processed_constrains = []

		for con_value in splited_constrains:
			v = con_value.split("/")
			if len(v) == 2:
				processed_constrains.append(self.__range(v, param))
			elif len(v) == 1:
				processed_constrains.append(self.__equality(v[0], param))
			else:
				raise Exception

		output = {
			"bool":
				{
					"should": processed_constrains,
					"minimum_should_match": 1
				}
		}
		return output

	def __parser(self, query):
		processed_conditions = []
		for key, value in query.items():
			if key.upper() in self.__slap_fields:
				output = self.__constrain_parser(value, self.__slap_fields[key.upper()]["slap_name"])
				processed_conditions.append(output)
			elif key.upper() == "VERSION":
				try:
					processed_value = toFloat(value)
					if processed_value in self.__supported_slap_versions:
						self.__output_api = toFloat(value)
					else:
						self.__error_list.append("The Version Number is not supported, using V1.0 protocol")
				except ValueError as e:
					self.__error_list.append("The Version Number is not correctly defined, using V1.0 protocol")

		if len(processed_conditions) > 0:
			output = {"query": {"bool": {"must": processed_conditions}}}
			self.query = output
		else:
			self.query = -1

