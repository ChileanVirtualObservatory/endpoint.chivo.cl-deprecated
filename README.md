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

### List of al catalogs:
   * WEB : http://dachs.lirae.cl:80/registry
   
   * Method: *GET*


### Table Access Protocol:

* Parameters : [DACHS](https://github.com/ChileanVirtualObservatory/dachs#parameters)

#### Service Capabilities:

   * WEB : http://dachs.lirae.cl:80/{catalog}/tap/capabilities
   
   * Method: *GET*

#### SYNC Query:

   * WEB : http://dachs.lirae.cl:80/{catalog}/tap/sync
   
   * Methond : *POST*
   
   * Return: *VOTABLE*

#### ASYNC Query:

##### New Query

   * WEB : http://dachs.lirae.cl:80/{catalog}/tap/async
   
   * Method : *POST*
   
   * RETURN : *VOTABLE* With query id
   
##### List Querys

   * WEB : http://dachs.lirae.cl:80/{catalog}/tap/async
 
   * Method: *GET*
   
   * Parameters: *None*

   * RETURN: *UWL* an xml with all querys with their status
   
##### Query Info
   * WEB : http://dachs.lirae.cl:80/{catalog}/tap/async/:id
   
   * Method: *GET*
   
   * Parameters: *None* 
   
   * RETURN :  *UWL* with query status
   
##### Other options

   * WEB : http://dachs.lirae.cl:80/{catalog}/tap/async/:id/:option
  
   * Parameters: `option phase , quote , executionduration , destruction , error , parameters , results , owner`   

   * Method: *GET*
   
###Simple Cone Search:
* Web: http://dachs.lirae.cl:80/{catalog}/scs

* Method: *GET*

* Attributes:
 * RA `Decimal degree`
 * DEC `Decimal degree`
 * SR `Decimal degree`
 * *Optional*:
   * VERB: `1 , 2 , 3`


###Simple Image Acess:
* Web: http://dachs.lirae.cl:80/{catalog}/sia

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

### Simple Spectral Access:
* Web: http://dachs.lirae.cl:80/{catalog}/ssa

* Method: *GET*

* Attributes:
	* POS = RA, DEC `Decimal degree`
		* *Ex*: 
			* POS=52,-27.8 
			* POS=52,-27.8;GALACTIC with GALACTIC the coordinate system 
	* SIZE `Degree`
		* *Ex*: 
			* SIZE=0.05
	* BAND `meters`
	 	* *Ex*: 
	 		* BAND=1E-7/3E-6
	 		* BAND=1E-7/3E-6;source 
	 		* BAND=1E-7/3E-6;observer
	* TIME `ISO 8601 UTC`
		* *Ex*: 
			* TIME = 1998-05-21/1999
	* Format 
		```
		all,
		compliant,
		native,
		graphic,
		votable,
		fits,
		xml,
		metadata
		```
	* *Optional*:
		* *TESTED*  
		* TARGETNAME `string`
		* REDSHIFT (dλ/λ) `string`
		* *NOT TESTED*
		* APERTURE `degree`
		* SPECRP `double`
		* TIMERES `double`

### External Registry

* Use  http://dachs.lirae.cl:80/external/URL, i.e  http://dachs.lirae.cl:80/external/registry , to se all catalogs
	


