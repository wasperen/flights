import requests
import pandas as pd
import csv

#"iata","airport","city","state","country","lat","long"
#"00M","Thigpen ","Bay Springs","MS","USA",31.95376472,-89.23450472
#"00R","Livingston Municipal","Livingston","TX","USA",30.68586111,-95.01792778

def find_timezone(lat, lon):
	response = requests.get('http://api.geonames.org/timezoneJSON?&username=wasperen&lat=' + str(lat) + '&lng=' + str(lon))
	return response

airports = pd.read_csv('airports.csv', delimiter=',', header = 0, quotechar = '"')
timezones = airports.apply(lambda r : find_timezone(r['lat'], r['long']), axis = 1)

timezones_resp = timezones.apply(lambda r : pd.Series(r.json()))
airports_timezones = airports.join(timezones_resp[['rawOffset', 'timezoneId']])

airports_timezones.to_csv('airports-timezones.csv', index = False, quoting = csv.QUOTE_NONNUMERIC, quotechar = '"')
