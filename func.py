from classes import Catalog, Registry 

#Functions for data streaming
def streamDataGet(r):
	#~ for line in r.iter_lines():
			#~ if line: # filter out keep-alive new lines
				#~ yield line
	return r

def streamDataPost(r):
	#~ CHUNK = 1024
	#~ for the_page in iter(lambda: r.read(CHUNK), ''):
		#~ yield the_page
	return r

def getResponseType(content):
	if "content-type" in content.keys():
		return content["content-type"].split(";")[0]
	else:
		return 'text/xml'
