from app.services.models import Catalog, Registry 

#Functions for data streaming

#Iters lines from GET response object
def streamDataGet(r):
	#for line in r.iter_lines():
	#		if line: # filter out keep-alive new lines
	#			yield line
	return r.text

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
