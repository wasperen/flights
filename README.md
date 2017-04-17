# Flights

These python scripts transform the flight history files found at http://stat-computing.org/dataexpo/2009/the-data.html

The script `transform-airports.py` adds the timezone data to the airports. This is done by using the API at http://www.geonames.org.

Then the output of that is used by `transform-flights.py` to extend the flight details with timezone data and airport names.

The shell script `transform-flights.sh` can be used to start the transformation of one single flight.csv file.
