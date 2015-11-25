primary_host = "http://otto.csrg.inf.utfsm.cl:9200/"
primary_index = "SL-Repository"
primary_mapping = "Spectral-Lines"
support_mapping = "support"

import elasticsearch
from multiprocessing import cpu_count
from multiprocess import Pool # Allows for efficient parallel Map, To install use pip install multiprocess

numeric_fields = ["WAVELENGHT", "FREQUENCY"]

class ElasticQuery():
    '''
    Class designed to retrieve easily SLAP data from Elasticsearch
    '''

    def __init__(self,host, primary_index, primary_mapping, support_mapping):
        self.__host = host
        self.__primary_index = primary_index.lower()
        self.__primary_mapping = primary_mapping
        self.__support_mapping = support_mapping
        self.__connection = elasticsearch.Elasticsearch(hosts=self.__host)
        self.__query_dic = {"query":{}}
        self.__max_result_size = self.__connection.count()["count"]
        self.__numeric_fields = numeric_fields

    def add_frequency_to_query(self, minimum=None, maximum=None):
        if not self.__query_dic["query"].has_key("range"):
            self.__query_dic["query"]["range"] = {}
        if minimum and maximum:
            self.__query_dic["query"]["range"]["Frequency"] = {"gte": minimum, "lte": maximum}
        elif maximum:
            self.__query_dic["query"]["range"]["Frequency"] = {"lte": maximum}
        elif minimum:
            self.__query_dic["query"]["range"]["Frequency"] = {"gte": minimum}
        else:
            raise ValueError("You must specify either a maximum or minimum")

    def add_wavelenght_to_query(self, minimum = None, maximum = None):
        if not self.__query_dic["query"].has_key("range"):
            self.__query_dic["query"]["range"] = {}
        if minimum and maximum:
            self.__query_dic["query"]["range"]["Wavelenght"] = {"gte" : minimum, "lte": maximum}
        elif maximum:
            self.__query_dic["query"]["range"]["Wavelenght"] = {"lte": maximum}
        elif minimum:
            self.__query_dic["query"]["range"]["Wavelenght"] = {"gte": minimum}
        else:
            raise ValueError("You must specify either a maximum or minimum")

    def __extractor(self, element):
        return element["_source"].values()



    def send_query(self,timeout=180):
        data = self.__connection.search(index=self.__primary_index, doc_type=self.__primary_mapping, body=self.__query_dic, size=self.__max_result_size,request_timeout=timeout)
        query_size = data["hits"]["total"]
        query_time = data["took"]
        query_data = data["hits"]["hits"]

        pool = Pool(cpu_count())
        filtered_data = pool.map(self.__extractor, query_data)
        pool.close()
        pool.join()
        data.clear()
        del query_data[:]

        #filtered_data = map(self.__extractor,query_data)
        return {"results":filtered_data,"time":query_time,"total":query_size}

    def range(self, limits, param):
        q = {}
        if limits[0] and limits[1]:
            q = {"gte": float(limits[0]), "lte": float(limits[1])}
        elif limits[1]:
            q = {"lte": float(limits[1])}
        elif limits[0]:
            q = {"gte": float(limits[0])}
        else:
            raise ValueError("You must specify either a maximum or minimum")

        return { "range" : { param : q }}

    def equality(self, value, param):
	    processed_value = value
	    if isinstance(value, list):
		    if param.upper() in numeric_fields:
			    processed_value = map(lambda x:float(x),value)
	    else:
		    if param.upper() in numeric_fields:
			    value = float(value)
	    return {"term": {param: processed_value}}

    def parser(self, query):
        for key, value in query.items():
            contrains = value.split(",")
            for con in contrains:
                v = con.split("/")
                if len(v)==2:
                    con_value = self.range(v,key)
                elif len(v)==1:
                    con_value = self.equality(v,key)
                else:
                    raise Exception



