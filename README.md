# Flask Endpoint

##Services

###Simple Cone Search:
* Web: http://dachs.lirae.cl:5000/alma/scs

* Method: *GET*

* Attributes:
 * RA `Decimal degree`
 * DEC `Decimal degree`
 * SR `Decimal degree`
 * *Optional*:
   * VERB: `1 , 2 , 3`


###Simple Image Acess:
* Web: http://dachs.lirae.cl:5000/alma/sia

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
* Web: http://dachs.lirae.cl:5000/alma/ssa

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



