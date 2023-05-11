#Ref: Module10: Day3 > Activites > 10-Ins_Flask_with_ORM
# Import the dependencies.
import numpy as np
import datetime as dt
from pathlib import Path
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# Create reference to databased file path
hawaii_data_set_path = Path("../Resources/hawaii.sqlite")

# create engine to hawaii.sqlite
hawaii_sqlite_engine = create_engine(f"sqlite:///{hawaii_data_set_path}")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=hawaii_sqlite_engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
hawaii_sqlite_session = Session(hawaii_sqlite_engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcom to Honolulu, Hawaii Climate APP<br/>" 
        f"Available Routes:<br/>"
        f"1.) /api/v1.0/precipitation  - gives precipitation analysis<br/>"
        f"2.) /api/v1.0/stations       - gives list of stations<br/>"
        f"3.) /api/v1.0/tobs           - gives one year of temprature data for the most active station<br/>"
        f"4.) /api/v1.0/<start_date>   - gives Min,Max,Avg Temprature from the Start date use yyyy-mm-dd date foramt<br/>"
        f"5.) /api/v1.0/<start>/<end>  - gives Min,Max,Avg Temprature for given date range(start/end) use yyyy-mm-dd date foramt<br/>"
    )

# precipitation route - returns json with the date as the key and the value as the precipitation for the last year in the database
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Get the most recent date from the data set and find one year from the recent date (12 months data)
    most_recent_date =dt.datetime.strptime(hawaii_sqlite_session.query(func.max(measurement.date)).scalar(),'%Y-%m-%d')
    one_year_from_lastdate = get_one_year_from_recent_date(most_recent_date)

    # Perform a query to retrieve the date and precipitation scores in to a dictionary
    one_year_query_result = dict(hawaii_sqlite_session.query(measurement.date,measurement.prcp).\
                        filter(measurement.date >= one_year_from_lastdate))
    
    close_session() # close the session

    # return the response
    return jsonify(one_year_query_result)

# stations route - returns jsonified data of all of the stations in the database 
@app.route("/api/v1.0/stations")
def stations():
    # Query the station details from the dataset
    station_infoResults = hawaii_sqlite_session.query(station.id,station.station,station.name).all()

    close_session() # close the session

    #Create a dictonary from the query result and append the station info list
    station_info = []
    for id,stat,name in station_infoResults:
        station_info_dict = {}
        station_info_dict["station_id"] = id
        station_info_dict["station_name"] = name
        station_info_dict["station"] = stat
        station_info.append(station_info_dict)

    # return the response   
    return jsonify(station_info)

# tobs route - returns jsonified data for the most active station for the last year
@app.route("/api/v1.0/tobs")
def tobs():
    # Get the most active station
    most_active_station = hawaii_sqlite_session.query(measurement.station).\
                        group_by(measurement.station).order_by(func.count(measurement.id).desc()).first()
    
    # Get the most recent date for the most active station 
    most_active_stationLatestDate =dt.datetime.strptime(hawaii_sqlite_session.query(func.max(measurement.date)).\
                                    filter(measurement.station ==most_active_station[0] ).scalar(), '%Y-%m-%d')
    # Find the date one year from the recent date for the most active station
    most_active_station_last_12_month_date = get_one_year_from_recent_date(most_active_stationLatestDate)

    # Perform a query to retrieve 12 months of temperature data with date for the most active station
    most_active_station_oneyear_tobs_query_result = dict(hawaii_sqlite_session.query(measurement.date,measurement.tobs).\
                                                filter(measurement.date >= most_active_station_last_12_month_date).\
                                                filter(measurement.station == most_active_station[0]).all())
   
    # Get the station info for the most active station
    most_active_station_info = hawaii_sqlite_session.query(station.id,station.station,station.name).\
                                filter(station.station == most_active_station[0]).first()   
   
    close_session() # close the session

    #Create a dictonary from the query result. Append the station info to temperature data 
    tobs_info_dict = {}
    tobs_info_dict["station_id"] = most_active_station_info[0]
    tobs_info_dict["station"] = most_active_station_info[1]
    tobs_info_dict["station_name"] = most_active_station_info[2]
    tobs_info_dict["temperature_data_for_last_12_months"] = most_active_station_oneyear_tobs_query_result
    
    # return the response   
    return jsonify(tobs_info_dict)

# start route - accepts the start date as a parameter from the URL and returns the min, max, and average temperatures calculated from the given start date to the end of the dataset
@app.route("/api/v1.0/<start_date>")
def dynamic_start_date(start_date):

    #get min, maxand avg temperature for the date specified
    min_max_avg_temp_Info = get_min_max_avg_temp_info(start_date,dt.date.today())

    # return the response
    return jsonify(min_max_avg_temp_Info)

# start/end route - accepts the start and end dates as parameters from the URL and returns the min, max, and average temperatures calculated from the given start date to the given end date
@app.route("/api/v1.0/<start>/<end>")
def dynamic_start_end_date(start, end):
    
    #get min, maxand avg temperature for the date specified
    min_max_avg_temp_Info = get_min_max_avg_temp_info(start,end)

    # return the response
    return jsonify(min_max_avg_temp_Info)


# Reuable function to calculate min, max, avg temperature for the given date
def get_min_max_avg_temp_info(from_date,to_date):

    #  query by joining station and measurement table and get the station info and min, max and avg temperature for the given date
    min_max_avg_temp_list = hawaii_sqlite_session.query(measurement.date, measurement.station, func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs),station.name,func.count(measurement.station)).\
                                filter(measurement.station == station.station).group_by(measurement.station).filter(measurement.date >= from_date).filter(measurement.date <= to_date).\
                                    order_by(measurement.date).all()
        
    close_session() # close the session

    # create a return list to the query result in form of dictonary data
    return_list = []

    # loop through each record from the query and create a dict data
    for dt, stat, min, max, avg, name, count in min_max_avg_temp_list:
        return_list_dict = {}
        return_list_dict["date"] = dt
        return_list_dict["station"] = stat
        return_list_dict["station_min_temp"] = min
        return_list_dict["station_max_temp"] = max
        return_list_dict["station_avg_temp"] = avg
        return_list_dict["station_name"] = name
        return_list_dict["count_of_climate_record"] = count    

        # add the dict data to the return lists
        return_list.append(return_list_dict)

    # return the response  
    return(return_list)

# Reuable function to calculate one year from most recent date
def get_one_year_from_recent_date(recent_date):

    # Get the that is one year from the recent date (12 months)
    return_one_year_from_lastdate = dt.date(recent_date.year-1, recent_date.month, recent_date.day)

    # return the response
    return (return_one_year_from_lastdate)


def close_session():
    # close Session
    hawaii_sqlite_session.close()

if __name__ == '__main__':
    app.run(debug=True)



