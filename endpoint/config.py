#Enabling the development enviroment
DEBUG = True

#Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 4

# Enable protection agains *Cross-site Request Forgery (CSRF)*
#CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
#CSRF_SESSION_KEY = "12c4bf6531cb3aeafca38c742f06294555b5dd17042185faf01b106d60e8e42f2334721c11963ead126b47002bfd7ddaaa6d53fbf9a831243cc5c0ab0491bae6"

# Secret key for signing cookies
#SECRET_KEY = "08cca79fecaffbfdba7dead9f0c9e1fb156f67c8a99d3162f7f44930634e4f5422967531589d7feb3786618f61a0bc7cd78149c9511395c645bfef6ea47645e1"

CHIVO_URL = "http://endpoint.lirae.cl"

#Dachs servers
DACHS_SERVERS = []
DACHS_SERVERS.append(
 	{'shortname': 'alma', 
 	'title': 'Chilean Virtual Observatory, Alma Cycle 0',
 	'capabilities':
 		{
 		'tap':'http://alma-be.lirae.cl:8080/__system__/tap/run/tap',
		'scs':'http://alma-be.lirae.cl:8080/cycle0fits/q/scs-cycle0-fits/scs.xml?',
 		'sia':'http://alma-be.lirae.cl:8080/cycle0fits/q/siap-cycle0-fits/siap.xml?'
 		 },
 	'filePath': 'http://alma-be.lirae.cl:8080/getproduct/cycle0fits'
 	}
)

#Registry URL
REG_URL = "http://alma-be.lirae.cl:8080/oai.xml"

