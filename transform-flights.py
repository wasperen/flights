import fileinput
from io import StringIO
import pandas as pd
import datetime as dt
import csv
import math
import sys

# Year,Month,DayofMonth,DayOfWeek,DepTime,CRSDepTime,ArrTime,CRSArrTime,UniqueCarrier,FlightNum,TailNum,ActualElapsedTime,CRSElapsedTime,AirTime,ArrDelay,DepDelay,Origin,Dest,Distance,TaxiIn,TaxiOut,Cancelled,CancellationCode,Diverted,CarrierDelay,WeatherDelay,NASDelay,SecurityDelay,LateAircraftDelay
# 1987,10,14,3,741,730,912,849,PS,1451,NA,91,79,NA,23,11,SAN,SFO,447,NA,NA,0,NA,0,NA,NA,NA,NA,NA
# 1987,10,15,4,729,730,903,849,PS,1451,NA,94,79,NA,14,-1,SAN,SFO,447,NA,NA,0,NA,0,NA,NA,NA,NA,NA
# 1987,10,17,6,741,730,918,849,PS,1451,NA,97,79,NA,29,11,SAN,SFO,447,NA,NA,0,NA,0,NA,NA,NA,NA,NA

airports = pd.read_csv('airports-timezones.csv', delimiter=',', header = 0, quotechar = '"').set_index('iata')
carriers = pd.read_csv('carriers.csv', delimiter=',', header = 0, quotechar = '"').set_index('Code')
names = ["Year","Month","DayofMonth","DayOfWeek","DepTime","CRSDepTime","ArrTime","CRSArrTime","UniqueCarrier","FlightNum","TailNum","ActualElapsedTime","CRSElapsedTime","AirTime","ArrDelay","DepDelay","Origin","Dest","Distance","TaxiIn","TaxiOut","Cancelled","CancellationCode","Diverted","CarrierDelay","WeatherDelay","NASDelay","SecurityDelay","LateAircraftDelay"]

def create_timestamp(year, month, day, time, offset):
    if math.isnan(time) or math.isnan(offset):
        return float('nan')
    (fraction,integer) = math.modf(offset)
    offset_hours = math.trunc(integer)
    offset_minutes = math.trunc(fraction * 60)
    try:
        return dt.datetime(
                year = year, month = month, day = day,
                hour = (time // 100) % 24, minute = time % 100, 
                tzinfo = dt.timezone(offset = dt.timedelta(hours = offset_hours, minutes = offset_minutes))
        )
    except:
        print(year, month, day, time, offset, file=sys.stderr)

for line in fileinput.input():
    buf = StringIO(line)
    flight = pd.read_csv(buf, quotechar = '"', names = names)
    flight_enriched = flight \
            .join(airports, on = 'Origin', rsuffix = '_origin') \
            .join(airports, on = 'Dest', rsuffix = '_dest') \
            .join(carriers, on = 'UniqueCarrier')
    flight_times = flight_enriched.assign(
            DepartureTS    = lambda r : create_timestamp(r['Year'][0], r['Month'][0], r['DayofMonth'][0], r['DepTime'][0],    r['rawOffset'][0]),
            CRSDepartureTS = lambda r : create_timestamp(r['Year'][0], r['Month'][0], r['DayofMonth'][0], r['CRSDepTime'][0], r['rawOffset'][0]),
            ArrivalTS      = lambda r : create_timestamp(r['Year'][0], r['Month'][0], r['DayofMonth'][0], r['ArrTime'][0],    r['rawOffset_dest'][0]),
            CRSArrivalTS   = lambda r : create_timestamp(r['Year'][0], r['Month'][0], r['DayofMonth'][0], r['CRSArrTime'][0], r['rawOffset_dest'][0])
    )
    buf = StringIO("")
    flight_times.to_csv(buf, index = False, header = False, quoting = csv.QUOTE_MINIMAL, quotechar = '"', na_rep = '',
            columns = [
                    'DepartureTS', 'CRSDepartureTS', 'ArrivalTS', 'CRSArrivalTS',
                    "UniqueCarrier","Description", "FlightNum","TailNum",
                    "Origin","airport","city","state","lat","long","rawOffset","timezoneId",
                    "Dest","airport_dest","city_dest","state_dest","lat_dest","long_dest","rawOffset_dest","timezoneId_dest",
                    "Cancelled","CancellationCode","Diverted",
                    "TaxiIn","TaxiOut",
                    "Distance",
                    "ActualElapsedTime","CRSElapsedTime","AirTime","ArrDelay","DepDelay",
                    "CarrierDelay","WeatherDelay","NASDelay","SecurityDelay","LateAircraftDelay"])
    print(buf.getvalue(), end = '')
