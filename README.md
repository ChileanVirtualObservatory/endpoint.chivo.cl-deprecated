# Flask Endpoint

##Requeriments

###Python Requirements
* Python >= 2.7 
* [Python Flask](http://flask.pocoo.org/)
* [Python requests](http://docs.python-requests.org/en/latest/)
* Python urllib
* Python urllib2
* Python json

###For deployment
* [Apache web Server](http://httpd.apache.org/)
* [wsgi_mod](http://flask.pocoo.org/docs/deploying/mod_wsgi/)



##For Develop and testing
* First clone the repo

    git clone git@github.com:ChileanVirtualObservatory/flask_endpoint.git

* Open a terminal and run *endpoint.py*

    python endpoint.py

* The webserver will be running in *localhost:5000/*

##Deployment

* First clone the repo

    git clone git@github.com:ChileanVirtualObservatory/flask_endpoint.git

* Edit *endpoint.wsgi* with the file's path

    sys.path.insert(0,"/var/www/flask_endpoint")

* [Configure Apache](http://flask.pocoo.org/docs/deploying/mod_wsgi/#configuring-apache)

##Services

### Table Access Protocol:

* Parameters : [DACHS](https://github.com/ChileanVirtualObservatory/dachs#parameters)

#### Service Capabilities:

   * WEB : http://endpoint.lirae.cl/alma/tap/capabilities
   
   * Method: *GET*

#### SYNC Query:

   * WEB : http://endpoint.lirae.cl/alma/tap/sync
   
   * Methond : *POST*
   
   * Return: *VOTABLE*

#### ASYNC Query:

##### New Query

   * WEB : http://endpoint.lirae.cl/alma/tap/async
   
   * Method : *POST*
   
   * RETURN : *VOTABLE* With query id
   
##### List Querys

   * WEB : http://endpoint.lirae.cl/alma/tap/async
 
   * Method: *GET*
   
   * Parameters: *None*

   * RETURN: *UWL* an xml with all querys with their status
   
##### Query Info
   * WEB : http://endpoint.lirae.cl/alma/tap/async/:id
   
   * Method: *GET*
   
   * Parameters: *None* 
   
   * RETURN :  *UWL* with query status
   
##### Other options

   * WEB : http://endpoint.lirae.cl/alma}/tap/async/:id/:option
  
   * Parameters: `option phase , quote , executionduration , destruction , error , parameters , results , owner`   

   * Method: *GET*
   
###Simple Cone Search:
* Web: http://endpoint.lirae.cl/alma/scs

* Method: *GET*

* Attributes:
 * RA `Decimal degree`
 * DEC `Decimal degree`
 * SR `Decimal degree`
 * *Optional*:
   * VERB: `1 , 2 , 3`


###Simple Image Acess:
* Web: http://endpoint.lirae.cl/alma/sia

* Method: *GET*

* Attributes: 
 * POS = RA,DEC `Decimal degree`
 * SIZE `Degree`
 * *Optional*:
	* INTERSECT `COVERS , ENCLOSED , CENTER , OVERLAPS`
	* NAXIS = <width>,<height> `pixels`
	* CFRAME `ICRS, FK5, FK4, ECL, GAL , SGAL`
	* EQUINOX `?`
	* CRPIX `?`
	* CRVAL `?`
	* CDELT `?`
	* ROTANG `degree`
	* PROJ `TAN , SIN , ARC`
	* FORMAT `image/fits, image/png, image/jpeg, text/html, ALL, GRAPHIC, GRAPHIC-<SOMETHING>, METADATA`
	* VERB `1 , 2 , 3`

### External 

#### Get External JSON Services

* To get specific Service (not all the data, just Shortname, Title, and AccessUrl)

	 http://endpoint.lirae.cl/external/{service} , service can be tap,scs,sia,ssa
	

### Harvesting Interface

* Registry harvesting interface

	http://endpoint.lirae.cl/oai.xml?


