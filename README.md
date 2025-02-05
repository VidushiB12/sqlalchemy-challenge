# sqlalchemy-challenge

Using flask, the following endpoints are built:

/api/v1.0/precipitation<br/>
/api/v1.0/stations<br/>
/api/v1.0/tobs<br/>
/api/v1.0/start<br/>
/api/v1.0/start/end

The home page shows all the endpoints that can be accessed.

The precipitation endpoint returns the precipitation together with the date in the form of a dictionary for the past year from the most recent date in the data set.

The stations endpoint returns the lists of stations from the dataset.

The tobs endpoint returns the temperatures from the most active station.

The start endpoint returns the minimum, average and maximum temperatures from a given start date. The start date must be in the format dd-mm-yyyy. 

The start and end endpoint returns the minimum, average and maximum temperatures for that specific period. 

All dates must be in the format dd-mm-yyyy.

